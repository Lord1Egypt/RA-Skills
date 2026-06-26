#!/usr/bin/env python3
"""ClawPhone 单元测试"""

import sys
from pathlib import Path

# 添加 skill 根目录到 path
sys.path.insert(0, str(Path(__file__).parent.parent))

from adapter.clawphone import (
    ClawPhone,
    register,
    lookup,
    call,
    set_status,
    _phone
)
import sqlite3

DB_PATH = Path.home() / ".openclaw" / "skills" / "clawphone" / "phonebook.db"


def clear_db():
    """清空测试数据库"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM phones")
    cur.execute("DELETE FROM call_log")
    conn.commit()
    conn.close()


def test_register():
    print("测试: 注册号码...")
    clear_db()
    phone_id = register("testalias")
    assert phone_id.isdigit() and len(phone_id) == 13, f"格式错误: {phone_id}"
    print(f"  [OK] 注册成功: {phone_id}")

    # 再次注册应返回已有号码
    phone_id2 = register("testalias")
    assert phone_id == phone_id2, "重复注册应返回相同号码"
    print("  [OK] 重复注册返回相同号码")


def test_lookup():
    print("测试: 查询...")
    clear_db()
    phone_id = register("alice")
    node_id = "CL-01S-ALICE-001"
    # 插入一条带 node_id 的记录
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE phones SET node_id = ? WHERE phone_id = ?", (node_id, phone_id))
    conn.commit()
    conn.close()

    # 通过 phone_id 查询
    found = lookup(phone_id)
    assert found == node_id, f"查询失败: {found} != {node_id}"
    print(f"  [OK] 通过 phone_id 查到 node_id: {found}")

    # 通过 alias 查询
    found2 = lookup("alice")
    assert found2 == node_id, f"别名查询失败: {found2}"
    print(f"  [OK] 通过别名查到 node_id: {found2}")


def test_set_status():
    print("测试: 状态设置...")
    set_status("online")
    assert _phone._status == "online"
    print("  [OK] 状态更新为 online")
    set_status("away")
    assert _phone._status == "away"
    print("  [OK] 状态更新为 away")


def test_call_basic():
    print("测试: 呼叫（无网络）...")
    clear_db()
    my_phone = register("bob")
    # 不注入网络，直接调用应失败
    result = call("0000000000000", "hello")  # 13位不存在号码
    assert result is False, "无网络时应返回 False"
    print("  [OK] 无网络时呼叫失败 (预期)")


def test_invalid_alias():
    print("测试: 非法 alias...")
    try:
        register("abc def")  # 有空格
        assert False, "应抛出异常"
    except ValueError:
        print("  [OK] 正确拒绝非法 alias")


if __name__ == "__main__":
    print("=== ClawPhone 单元测试 ===\n")
    try:
        test_register()
        test_lookup()
        test_set_status()
        test_call_basic()
        test_invalid_alias()
        print("\n[OK] 所有测试通过！")
    except AssertionError as e:
        print(f"\n[FAIL] 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] 意外错误: {e}")
        sys.exit(1)
