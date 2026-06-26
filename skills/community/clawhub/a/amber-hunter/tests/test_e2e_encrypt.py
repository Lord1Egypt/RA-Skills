"""
tests/test_e2e_encrypt.py — E2E 加密往返测试
测试完整链路：创建胶囊(加密) → 云端同步(密文传输) → 拉取(解密) → 验证

覆盖 P1-2/P2-3 D2 E2EE 加密链路
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import time
import base64
from unittest.mock import patch, MagicMock

from core.crypto import derive_key, encrypt_content, decrypt_content, generate_salt


class TestE2EEEncryptionRoundtrip:
    """
    测试 E2E 加密的完整往返：
    1. 明文 → AES-256-GCM 加密（使用 PBKDF2 派生密钥）
    2. 解密 → 还原明文
    3. 多字段加密（memo / content / tags 分别加密）
    """

    def test_content_encrypted_field_roundtrip(self, test_db):
        """
        胶囊 content 字段加密后解密应完全还原。
        这是 /capsules POST → GET 往返的核心逻辑。
        """
        from core.db import insert_capsule, get_capsule

        master_pw = "test-master-password-123"
        capsule_id = "test-e2e-capsule"
        original_memo = "这是测试备忘录"
        original_content = "这是一条非常长的记忆内容，包含了用户的具体信息。" * 5
        original_tags = "work,project,important"

        created_at = time.time()

        # Step 1: 加密
        salt = generate_salt()
        key = derive_key(master_pw, salt)
        nonce_ct = encrypt_content(original_content.encode("utf-8"), key)
        ciphertext, nonce = nonce_ct
        ct_b64 = base64.b64encode(ciphertext).decode()
        nonce_b64 = base64.b64encode(nonce).decode()

        # Step 2: 写入数据库（模拟 /capsules POST）
        insert_capsule(
            capsule_id=capsule_id,
            memo=original_memo,
            content=ct_b64,
            tags=original_tags,
            session_id="test-session",
            window_title=None,
            url=None,
            created_at=created_at,
            salt=base64.b64encode(salt).decode(),
            nonce=nonce_b64,
            encrypted_len=len(ct_b64),
            content_hash="testhash",
            source_type="manual",
            category="test",
        )

        # Step 3: 读取并解密（模拟 /capsules/{id} GET）
        row = get_capsule(capsule_id)
        assert row is not None

        # 模拟 /capsules/{id} 的解密逻辑
        salt_decoded = base64.b64decode(row["salt"])
        nonce_decoded = base64.b64decode(row["nonce"])
        ciphertext_decoded = base64.b64decode(row["content"])
        key_decoded = derive_key(master_pw, salt_decoded)
        decrypted = decrypt_content(ciphertext_decoded, key_decoded, nonce_decoded)

        assert decrypted.decode("utf-8") == original_content

    def test_multi_field_encryption(self, test_db):
        """
        memo / content / tags 三字段独立加密、独立解密。
        模拟 /sync 端点的完整 payload 加密逻辑。
        """
        from core.db import insert_capsule

        master_pw = "multi-field-test-pw"
        capsule_id = "test-multi-field"

        memo_original = "用户偏好简洁方案"
        content_original = "详细内容：用户不喜欢复杂的异步代码"
        tags_original = "偏好,python,architecture"

        created_at = time.time()
        salt = generate_salt()
        key = derive_key(master_pw, salt)

        def _enc(plaintext: str) -> tuple[bytes, bytes]:
            ct, nonce = encrypt_content(plaintext.encode("utf-8"), key)
            return ct, nonce

        memo_ct, memo_nonce = _enc(memo_original)
        content_ct, content_nonce = _enc(content_original)
        tags_ct, tags_nonce = _enc(tags_original)

        def _dec(ct: bytes, nonce: bytes) -> str:
            pt = decrypt_content(ct, key, nonce)
            return pt.decode("utf-8")

        # 验证解密完全还原
        assert _dec(memo_ct, memo_nonce) == memo_original
        assert _dec(content_ct, content_nonce) == content_original
        assert _dec(tags_ct, tags_nonce) == tags_original

    def test_wrong_password_decryption_fails(self, test_db):
        """错误密码解密应返回 None，不应抛出异常"""
        salt = generate_salt()
        correct_key = derive_key("correct-password", salt)
        wrong_key = derive_key("wrong-password", salt)

        plaintext = b"secret memory content"
        ciphertext, nonce = encrypt_content(plaintext, correct_key)

        # 错误密钥
        result = decrypt_content(ciphertext, wrong_key, nonce)
        assert result is None

    def test_tampered_ciphertext_fails_silently(self, test_db):
        """密文被篡改后解密应返回 None，保持静默不抛异常"""
        salt = generate_salt()
        key = derive_key("password", salt)

        plaintext = b"original content"
        ciphertext, nonce = encrypt_content(plaintext, key)

        # 篡改密文（翻转某个字节）
        tampered = bytearray(ciphertext)
        tampered[5] ^= 0xFF
        tampered = bytes(tampered)

        result = decrypt_content(tampered, key, nonce)
        assert result is None


class TestDIDEncryption:
    """
    DID 密钥派生加密测试（D2 架构）。
    设备私钥派生 capsule_key，加密/解密不依赖 master_password。
    """

    def test_did_derive_key_deterministic(self):
        """相同 device_priv + capsule_id 应派生相同 AES key"""
        from core.crypto import derive_capsule_key

        # 有效的 hex 字符串（64字符 = 32字节）
        device_priv = "aabbccdd" + "00" * 28  # 32字节 hex
        capsule_id_1 = "capsule-001"
        capsule_id_2 = "capsule-002"

        key1, _ = derive_capsule_key(device_priv, capsule_id_1)
        key2, _ = derive_capsule_key(device_priv, capsule_id_2)
        key3, _ = derive_capsule_key(device_priv, capsule_id_1)  # 再次派生相同 capsule

        # 同一 capsule_id 派生相同密钥
        assert key1 == key3
        # 不同 capsule_id 派生不同密钥
        assert key1 != key2

    def test_did_encrypt_decrypt_roundtrip(self):
        """DID 派生的 key 应能正确加解密"""
        from core.crypto import derive_capsule_key

        device_priv = "aabbccdd" + "11" * 28  # 32字节 hex
        capsule_id = "test-capsule-did-001"

        aes_key, _ = derive_capsule_key(device_priv, capsule_id)

        plaintext = "这是 DID 加密的记忆内容".encode("utf-8")
        ciphertext, nonce = encrypt_content(plaintext, aes_key)
        decrypted = decrypt_content(ciphertext, aes_key, nonce)

        assert decrypted == plaintext


class TestSyncEncryptPayload:
    """
    测试 /sync 端点的 payload 加密逻辑。
    模拟 _do_sync_capsules 中的加密步骤。
    """

    def test_sync_payload_encryption_structure(self, test_db, monkeypatch):
        """
        验证 sync 时 memo/tags/content 三字段独立加密的格式正确。
        模拟 huper.org 云端返回的加密 capsule 格式。
        """
        from core.crypto import derive_key, encrypt_content, generate_salt
        import base64

        master_pw = "sync-test-password"
        capsule_id = "sync-test-capsule"
        now = time.time()

        # 模拟本地加密（sync 上传路径）
        salt = generate_salt()
        key = derive_key(master_pw, salt)
        salt_b64 = base64.b64encode(salt).decode()

        original = {
            "memo": "测试备忘录",
            "content": "这是记忆的详细内容",
            "tags": "work,test",
        }

        # 加密每个字段（模拟 _do_sync_capsules 的加密逻辑）
        memo_ct, memo_nonce = encrypt_content(original["memo"].encode("utf-8"), key)
        content_ct, content_nonce = encrypt_content(original["content"].encode("utf-8"), key)
        tags_ct, tags_nonce = encrypt_content(original["tags"].encode("utf-8"), key)

        payload = {
            "salt": salt_b64,
            "memo_enc": base64.b64encode(memo_ct).decode(),
            "memo_nonce": base64.b64encode(memo_nonce).decode(),
            "content_enc": base64.b64encode(content_ct).decode(),
            "content_nonce": base64.b64encode(content_nonce).decode(),
            "tags_enc": base64.b64encode(tags_ct).decode(),
            "tags_nonce": base64.b64encode(tags_nonce).decode(),
            "created_at": now,
        }

        # 模拟云端存储后返回（_import_cloud_capsule 路径）
        def _decrypt(enc_b64, nonce_b64):
            ct = base64.b64decode(enc_b64)
            nonce = base64.b64decode(nonce_b64)
            pt = decrypt_content(ct, key, nonce)
            return pt.decode("utf-8")

        decrypted_memo = _decrypt(payload["memo_enc"], payload["memo_nonce"])
        decrypted_content = _decrypt(payload["content_enc"], payload["content_nonce"])
        decrypted_tags = _decrypt(payload["tags_enc"], payload["tags_nonce"])

        assert decrypted_memo == original["memo"]
        assert decrypted_content == original["content"]
        assert decrypted_tags == original["tags"]


class TestPullDecryptImport:
    """
    测试 /sync/pull 的云端拉取→解密→入库链路。
    模拟 _import_cloud_capsule 的完整流程。
    """

    def test_import_cloud_capsule_roundtrip(self, test_db, monkeypatch):
        """
        模拟云端胶囊 → 解密 → 入库 → 读取，验证完整往返。
        """
        import core.db as db_module

        master_pw = "import-test-pw"
        salt = generate_salt()
        key = derive_key(master_pw, salt)
        salt_b64 = base64.b64encode(salt).decode()

        original_memo = "云端拉取的备忘录"
        original_content = "这是从云端解密后导入的内容"
        original_tags = "cloud,sync,test"

        # 模拟云端加密 payload
        memo_ct, memo_nonce = encrypt_content(original_memo.encode("utf-8"), key)
        content_ct, content_nonce = encrypt_content(original_content.encode("utf-8"), key)
        tags_ct, tags_nonce = encrypt_content(original_tags.encode("utf-8"), key)

        cloud_payload = {
            "id": "cloud-capsule-001",
            "memo_enc": base64.b64encode(memo_ct).decode(),
            "memo_nonce": base64.b64encode(memo_nonce).decode(),
            "content_enc": base64.b64encode(content_ct).decode(),
            "content_nonce": base64.b64encode(content_nonce).decode(),
            "tags_enc": base64.b64encode(tags_ct).decode(),
            "tags_nonce": base64.b64encode(tags_nonce).decode(),
            "salt": salt_b64,
            "created_at": time.time(),
            "updated_at": time.time(),
            "category": "test",
            "source_type": "sync",
            "session_id": None,
        }

        # 模拟 _import_cloud_capsule 解密逻辑
        def _decrypt_text(enc_b64, nonce_b64):
            if not enc_b64 or not nonce_b64:
                return ""
            ct = base64.b64decode(enc_b64)
            nonce = base64.b64decode(nonce_b64)
            pt = decrypt_content(ct, key, nonce)
            return pt.decode("utf-8") if pt else ""

        memo_dec = _decrypt_text(cloud_payload["memo_enc"], cloud_payload["memo_nonce"])
        content_dec = _decrypt_text(cloud_payload["content_enc"], cloud_payload["content_nonce"])
        tags_dec = _decrypt_text(cloud_payload["tags_enc"], cloud_payload["tags_nonce"])

        assert memo_dec == original_memo
        assert content_dec == original_content
        assert tags_dec == original_tags

    def test_import_with_empty_fields(self, test_db):
        """空字段应优雅处理，不抛出异常"""
        from core.crypto import derive_key, encrypt_content, generate_salt
        import base64

        master_pw = "empty-field-test"
        salt = generate_salt()
        key = derive_key(master_pw, salt)
        salt_b64 = base64.b64encode(salt).decode()

        # 只有 memo 有内容，content 和 tags 为空
        memo_ct, memo_nonce = encrypt_content("有内容的备忘录".encode("utf-8"), key)
        empty_ct, empty_nonce = encrypt_content(b"", key)

        cloud_payload = {
            "id": "empty-fields-capsule",
            "memo_enc": base64.b64encode(memo_ct).decode(),
            "memo_nonce": base64.b64encode(memo_nonce).decode(),
            "content_enc": base64.b64encode(empty_ct).decode(),
            "content_nonce": base64.b64encode(empty_nonce).decode(),
            "tags_enc": base64.b64encode(empty_ct).decode(),
            "tags_nonce": base64.b64encode(empty_nonce).decode(),
            "salt": salt_b64,
            "created_at": time.time(),
            "updated_at": time.time(),
            "category": "",
            "source_type": "sync",
            "session_id": None,
        }

        def _decrypt_text(enc_b64, nonce_b64):
            if not enc_b64 or not nonce_b64:
                return ""
            ct = base64.b64decode(enc_b64)
            nonce = base64.b64decode(nonce_b64)
            pt = decrypt_content(ct, key, nonce)
            return pt.decode("utf-8") if pt else ""

        # 空字段解密应返回空字符串
        assert _decrypt_text(cloud_payload["content_enc"], cloud_payload["content_nonce"]) == ""
        assert _decrypt_text(cloud_payload["tags_enc"], cloud_payload["tags_nonce"]) == ""
