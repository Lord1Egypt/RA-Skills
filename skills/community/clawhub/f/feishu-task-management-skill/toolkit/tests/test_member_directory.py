import json
import pathlib
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from feishu_task_toolkit.members import MemberDirectory, build_member_table, fetch_authorized_scope
from feishu_task_toolkit.members import sync_members
from feishu_task_toolkit.config import ToolkitPaths, load_json


class MemberDirectoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.members = [
            {
                "open_id": "ou_alpha",
                "user_id": "u_alpha",
                "name": "张三",
                "en_name": "Zhang San",
                "nickname": "三哥",
                "email": "zhangsan@example.com",
                "mobile": "",
                "departments": ["研发部"],
                "department_ids": ["od_dev"],
                "status": "active",
            },
            {
                "open_id": "ou_beta",
                "user_id": "u_beta",
                "name": "张三",
                "en_name": "",
                "nickname": "",
                "email": "zhangsan2@example.com",
                "mobile": "",
                "departments": ["测试部"],
                "department_ids": ["od_test"],
                "status": "active",
            },
        ]

    def test_alias_resolution_takes_priority(self) -> None:
        directory = MemberDirectory(self.members, {"后端张三": "ou_alpha"})

        result = directory.resolve("后端张三")

        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["member"]["open_id"], "ou_alpha")

    def test_duplicate_name_reports_ambiguity(self) -> None:
        directory = MemberDirectory(self.members, {})

        result = directory.resolve("张三")

        self.assertEqual(result["status"], "ambiguous")
        self.assertEqual(len(result["candidates"]), 2)
        self.assertEqual({item["open_id"] for item in result["candidates"]}, {"ou_alpha", "ou_beta"})

    def test_build_member_table_merges_scope_and_department_records(self) -> None:
        scope_users = [
            {
                "open_id": "ou_alpha",
                "user_id": "u_alpha",
                "name": "张三",
                "email": "zhangsan@example.com",
                "department_ids": ["od_dev"],
                "departments": ["研发部"],
            }
        ]
        department_users = {
            "od_dev": [
                {
                    "open_id": "ou_alpha",
                    "user_id": "u_alpha",
                    "name": "张三",
                    "email": "zhangsan@example.com",
                    "department_ids": ["od_dev"],
                    "departments": ["研发部"],
                }
            ],
            "od_test": [
                {
                    "open_id": "ou_beta",
                    "user_id": "u_beta",
                    "name": "李四",
                    "email": "lisi@example.com",
                    "department_ids": ["od_test"],
                    "departments": ["测试部"],
                }
            ],
        }

        payload = build_member_table(scope_users, department_users)

        self.assertEqual(payload["version"], 1)
        self.assertEqual(len(payload["members"]), 2)
        self.assertEqual(payload["member_count"], 2)

    def test_load_aliases_from_disk_defaults_to_empty_mapping(self) -> None:
        directory = MemberDirectory(self.members, {})
        with tempfile.TemporaryDirectory() as temp_dir:
            alias_path = pathlib.Path(temp_dir) / "member_aliases.json"
            alias_path.write_text(json.dumps({"haojun": "ou_alpha"}), encoding="utf-8")

            loaded = directory.load_aliases(alias_path)

        self.assertEqual(loaded, {"haojun": "ou_alpha"})

    def test_sync_members_enriches_direct_scope_users_with_user_details(self) -> None:
        class FakeClient:
            def request(self, method, path, params=None, body=None, use_auth=True):
                if path == "/contact/v3/scopes":
                    return {"has_more": False, "user_ids": ["ou_alpha"], "department_ids": []}
                if path == "/contact/v3/users/ou_alpha":
                    return {
                        "user": {
                            "open_id": "ou_alpha",
                            "user_id": "u_alpha",
                            "name": "张三",
                            "email": "zhangsan@example.com",
                        }
                    }
                raise AssertionError(f"unexpected call: {path}")

        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            result = sync_members(FakeClient(), paths)
            members = load_json(paths.members_file, {"members": []})

        self.assertEqual(result["sync_meta"]["member_count"], 1)
        self.assertEqual(members["members"][0]["user_id"], "u_alpha")
        self.assertEqual(members["members"][0]["name"], "张三")

    def test_fetch_authorized_scope_uses_page_size_50(self) -> None:
        calls: list[dict[str, object]] = []

        class FakeClient:
            def request(self, method, path, params=None, body=None, use_auth=True):
                calls.append({"method": method, "path": path, "params": params})
                return {"has_more": False, "user_ids": [], "department_ids": []}

        fetch_authorized_scope(FakeClient())

        self.assertEqual(calls[0]["params"]["page_size"], 50)

    def test_sync_members_reports_sparse_profile_warning(self) -> None:
        class FakeClient:
            def request(self, method, path, params=None, body=None, use_auth=True):
                if path == "/contact/v3/scopes":
                    return {"has_more": False, "user_ids": ["ou_alpha"], "department_ids": []}
                if path == "/contact/v3/users/ou_alpha":
                    return {
                        "user": {
                            "open_id": "ou_alpha",
                            "user_id": "u_alpha",
                        }
                    }
                raise AssertionError(f"unexpected call: {path}")

        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            paths = ToolkitPaths(root=root, config_dir=root / "config", data_dir=root / "data")
            result = sync_members(FakeClient(), paths)

        self.assertTrue(result["sync_meta"]["warnings"])
        self.assertEqual(result["sync_meta"]["warnings"][0]["code"], "sparse_user_profiles")


if __name__ == "__main__":
    unittest.main()
