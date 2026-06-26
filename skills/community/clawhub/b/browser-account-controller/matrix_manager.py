#!/usr/bin/env python3
"""
浏览器账号控制器 - 多账号矩阵管理工具
通过 HTTP API 控制账号的启动、关闭和信息查询

重要：执行结果会同时打印到控制台和写入 last_result.txt 文件。
last_result.txt 文件由本脚本创建，位于本脚本所在目录。
"""

import requests
import json
import sys
import os
from typing import Dict, List, Optional, Tuple

# 获取脚本所在目录（last_result.txt 将写入此目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LAST_RESULT_FILE = os.path.join(SCRIPT_DIR, "last_result.txt")


def write_result(text: str) -> None:
    """
    将结果写入 last_result.txt 文件。
    文件位于本脚本所在目录，编码为 UTF-8。
    """
    with open(LAST_RESULT_FILE, "w", encoding="utf-8") as f:
        f.write(text)


class MatrixManager:
    """多账号矩阵管理器"""
    
    def __init__(self, api_url: str = "http://localhost:1008", timeout: int = 10):
        self.api_url = api_url
        self.timeout = timeout
        self.headers = {"Content-Type": "application/json; charset=utf-8"}
    
    def _make_request(self, payload: dict) -> dict:
        """底层方法：发送 HTTP 请求并返回解析后的 JSON 数据"""
        try:
            body_str = json.dumps(payload, ensure_ascii=False)
            body_bytes = body_str.encode('utf-8')
            
            resp = requests.post(
                self.api_url,
                data=body_bytes,
                headers=self.headers,
                timeout=self.timeout
            )
            resp.raise_for_status()
            return json.loads(resp.content.decode('utf-8'))
        except requests.exceptions.ConnectionError:
            raise Exception("无法连接到「多账号矩阵管理工具」（工具官网：https://zmt.scys6688.com/）。\n请确认：1. 软件已打开  2. 本地服务器已启动（端口1008）")
        except requests.exceptions.Timeout:
            raise Exception(f"请求超时（{self.timeout}秒），请检查网络或增加超时时间")
        except json.JSONDecodeError as e:
            raise Exception(f"响应解析失败: {e}")
        except Exception as e:
            raise Exception(f"请求失败: {e}")
    
    def get_all_accounts(self) -> Dict[str, str]:
        """获取所有账号信息"""
        data = self._make_request({"获取所有账号信息": []})
        return data.get("所有账号", {})
    
    def get_all_groups(self) -> List[str]:
        """获取所有分组"""
        data = self._make_request({"获取所有分组": []})
        groups = data.get("所有分组", {})
        return [groups[k] for k in sorted(groups.keys(), key=int)]
    
    def get_account_detail(self, index: str) -> dict:
        """获取账号详情"""
        return self._make_request({"指定账号所有数据": [index]})
    
    def find_account_index(self, keyword: str, accounts: Dict[str, str]) -> Optional[str]:
        """根据关键词查找账号索引（精准匹配优先，然后模糊匹配）"""
        if not accounts:
            return None
        
        # 精准匹配
        for idx, name in accounts.items():
            if name == keyword:
                return str(int(idx) + 1)
        
        # 模糊匹配
        matches = [(idx, name) for idx, name in accounts.items() if keyword in name]
        
        if len(matches) == 1:
            return str(int(matches[0][0]) + 1)
        elif len(matches) > 1:
            match_list = "\n".join([f"  [{int(idx)+1}] {name}" for idx, name in matches])
            raise Exception(f"找到多个匹配的账号，请输入完整账号名或索引：\n{match_list}")
        
        return None
    
    def start_account(self, index: str) -> dict:
        """启动账号"""
        return self._make_request({"启动": [index]})
    
    def stop_account(self, index: str) -> dict:
        """关闭账号"""
        return self._make_request({"关闭": [index]})
    
    def start_by_name(self, keyword: str) -> Tuple[dict, str, str]:
        """根据名称查找并启动账号"""
        accounts = self.get_all_accounts()
        index = self.find_account_index(keyword, accounts)
        
        if index is None:
            account_list = "\n".join([f"  [{int(idx)+1}] {name}" for idx, name in accounts.items()])
            raise Exception(f"未找到包含 '{keyword}' 的账号。\n可用账号：\n{account_list}")
        
        target_name = accounts.get(str(int(index) - 1), keyword)
        result = self.start_account(index)
        return result, index, target_name
    
    def stop_by_name(self, keyword: str) -> Tuple[dict, str, str]:
        """根据名称查找并关闭账号"""
        accounts = self.get_all_accounts()
        index = self.find_account_index(keyword, accounts)
        
        if index is None:
            account_list = "\n".join([f"  [{int(idx)+1}] {name}" for idx, name in accounts.items()])
            raise Exception(f"未找到包含 '{keyword}' 的账号。\n可用账号：\n{account_list}")
        
        target_name = accounts.get(str(int(index) - 1), keyword)
        result = self.stop_account(index)
        return result, index, target_name
    
    def list_accounts(self) -> str:
        """返回格式化的账号列表"""
        accounts = self.get_all_accounts()
        
        if not accounts:
            return "暂无账号"
        
        lines = ["当前所有账号："]
        for idx, name in sorted(accounts.items(), key=lambda x: int(x[0])):
            lines.append(f"  [{int(idx)+1}] {name}")
        
        return "\n".join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        usage = """用法: python matrix_manager.py <命令> [参数]

命令:
  list                    列出所有账号
  start <关键词>          按名称启动账号（先精准后模糊）
  start-index <索引>      按索引启动账号（如: 1, 2, 3）
  stop <关键词>           按名称关闭账号（先精准后模糊）
  stop-index <索引>       按索引关闭账号

文件:
  last_result.txt         执行结果输出文件（由本脚本创建，UTF-8编码）"""
        print(usage)
        write_result(usage)
        sys.exit(1)
    
    manager = MatrixManager()
    command = sys.argv[1].lower()
    result_text = ""
    
    try:
        if command == "list":
            result_text = manager.list_accounts()
            print(result_text)
        
        elif command == "start-index" and len(sys.argv) >= 3:
            index = sys.argv[2]
            try:
                int(index)
            except ValueError:
                result_text = f"[ERROR] 索引必须是数字，收到: {index}"
                print(result_text)
                write_result(result_text)
                sys.exit(1)
            result = manager.start_account(index)
            result_text = f"[OK] 成功启动账号 [{index}]"
            print(result_text)
            print(f"响应: {result}")
        
        elif command == "start" and len(sys.argv) >= 3:
            keyword = sys.argv[2]
            result, index, name = manager.start_by_name(keyword)
            result_text = f"[OK] 成功启动账号 [{index}] {name}"
            print(result_text)
            print(f"响应: {result}")
        
        elif command == "stop-index" and len(sys.argv) >= 3:
            index = sys.argv[2]
            try:
                int(index)
            except ValueError:
                result_text = f"[ERROR] 索引必须是数字，收到: {index}"
                print(result_text)
                write_result(result_text)
                sys.exit(1)
            result = manager.stop_account(index)
            result_text = f"[OK] 成功关闭账号 [{index}]"
            print(result_text)
            print(f"响应: {result}")
        
        elif command == "stop" and len(sys.argv) >= 3:
            keyword = sys.argv[2]
            result, index, name = manager.stop_by_name(keyword)
            result_text = f"[OK] 成功关闭账号 [{index}] {name}"
            print(result_text)
            print(f"响应: {result}")
        
        else:
            result_text = f"[ERROR] 未知命令: {command}"
            print(result_text)
            write_result(result_text)
            sys.exit(1)
        
        # 成功时写入结果
        write_result(result_text)
    
    except Exception as e:
        result_text = f"[ERROR] {e}"
        print(result_text)
        write_result(result_text)
        sys.exit(1)


if __name__ == "__main__":
    main()
