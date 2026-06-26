#!/usr/bin/env python3
"""
B站用户信息查询脚本

功能：
- 获取B站用户的粉丝数量
- 获取B站用户的关注数量
- 获取B站用户的用户名

使用方法：
    python bili_query.py --vmid <用户ID>
    python bili_query.py --vmid <用户ID> --info <fans|follows|name|all>
"""

import argparse
import json
import sys
import re
import requests


class BiliUserInfo:
    """B站用户信息查询类"""
    
    def __init__(self, vmid):
        """
        初始化
        
        Args:
            vmid (str): B站用户ID
        """
        self.vmid = str(vmid)
        self.stat_api = "https://api.bilibili.com/x/relation/stat"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.bilibili.com/",
            "Accept": "application/json, text/plain, */*"
        }
    
    def get_fans(self):
        """
        获取粉丝数量
        
        Returns:
            int: 粉丝数量，失败返回None
        """
        try:
            url = f"{self.stat_api}?vmid={self.vmid}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    return data["data"]["follower"]
                else:
                    return {"error": f"API错误: {data.get('message', '未知错误')}"}
            else:
                return {"error": f"HTTP错误: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"网络异常: {str(e)}"}
        except (json.JSONDecodeError, KeyError) as e:
            return {"error": f"数据解析错误: {str(e)}"}
    
    def get_follows(self):
        """
        获取关注数量
        
        Returns:
            int: 关注数量，失败返回None
        """
        try:
            url = f"{self.stat_api}?vmid={self.vmid}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    return data["data"]["following"]
                else:
                    return {"error": f"API错误: {data.get('message', '未知错误')}"}
            else:
                return {"error": f"HTTP错误: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"网络异常: {str(e)}"}
        except (json.JSONDecodeError, KeyError) as e:
            return {"error": f"数据解析错误: {str(e)}"}
    
    def get_name(self):
        """
        获取用户名（通过API接口）
        
        Returns:
            str: 用户名，失败返回None
        """
        # 使用B站用户信息API获取用户名
        url = f"https://api.bilibili.com/x/space/acc/info?mid={self.vmid}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    return data["data"]["name"]
                else:
                    return {"error": f"API错误: {data.get('message', '未知错误')}"}
            else:
                return {"error": f"HTTP错误: {response.status_code}"}
            
        except requests.RequestException as e:
            return {"error": f"网络请求错误: {str(e)}"}
        except (json.JSONDecodeError, KeyError) as e:
            return {"error": f"解析错误: {str(e)}"}
    
    def get_all_info(self):
        """
        获取所有信息
        
        Returns:
            dict: 包含所有用户信息的字典
        """
        result = {
            "vmid": self.vmid,
            "fans": self.get_fans(),
            "follows": self.get_follows(),
            "name": self.get_name()
        }
        return result


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="查询B站用户信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s --vmid 8047632
  %(prog)s --vmid 8047632 --info fans
  %(prog)s --vmid 8047632 --info name
        """
    )
    
    parser.add_argument(
        "--vmid",
        required=True,
        help="B站用户ID（必填）"
    )
    
    parser.add_argument(
        "--info",
        choices=["fans", "follows", "name", "all"],
        default="all",
        help="查询的信息类型：fans(粉丝数)、follows(关注数)、name(用户名)、all(全部，默认)"
    )
    
    args = parser.parse_args()
    
    # 创建查询实例
    bili = BiliUserInfo(args.vmid)
    
    # 根据参数查询相应信息
    if args.info == "all":
        result = bili.get_all_info()
    elif args.info == "fans":
        result = {
            "vmid": args.vmid,
            "fans": bili.get_fans()
        }
    elif args.info == "follows":
        result = {
            "vmid": args.vmid,
            "follows": bili.get_follows()
        }
    elif args.info == "name":
        result = {
            "vmid": args.vmid,
            "name": bili.get_name()
        }
    
    # 输出JSON格式结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
