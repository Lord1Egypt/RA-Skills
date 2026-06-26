#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
东论发帖脚本
用于在东方热线论坛发布新帖子
使用预先配置的 token 直接发帖，无需登录
"""

import argparse
import json
import sys
import os
import urllib.request
from typing import Dict, Optional

# Windows 下设置 UTF-8 编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


# ==================== 配置区域 ====================

# 发帖接口
POST_API = "https://dzapi.cnool.net/home/skill/post_to_forum"

# 回帖接口
REPLY_API = "https://dzapi.cnool.net/home/skill/reply_to_forum"

# 热帖列表接口
HOT_ARTICLES_API = "https://dzapi.cnool.net/home/skill/hot_articles"

# 帖子详情接口
VIEW_ARTICLE_API = "https://dzapi.cnool.net/home/skill/view_article"

# 回复列表接口
VIEW_REPLIES_API = "https://dzapi.cnool.net/home/skill/view_replies"

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")

# =====================================================================


def load_config() -> Dict:
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
    return {}


def save_config(config: Dict):
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"保存配置文件失败: {e}")


class DonglunAPI:
    """东论 API 客户端"""

    def __init__(self, token: str):
        self.token = token

    def get_headers(self) -> Dict[str, str]:
        """构造请求头"""
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

    def make_request(self, url: str, data: Dict) -> Dict:
        """发送 HTTP POST 请求"""
        headers = self.get_headers()
        encoded_data = json.dumps(data).encode('utf-8')

        request = urllib.request.Request(
            url,
            data=encoded_data,
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                result = response.read().decode('utf-8')
                try:
                    return json.loads(result)
                except json.JSONDecodeError:
                    return {"raw": result, "success": True}
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8', errors='ignore')
            try:
                error_json = json.loads(error_body)
                return {"error": error_json}
            except:
                return {"error": f"HTTP {e.code}: {e.reason}", "details": error_body[:500]}
        except Exception as e:
            return {"error": str(e)}

    def get_hot_articles(self, days: int = 7, pageIndex: int = 1, pageSize: int = 20) -> Dict:
        """
        获取热帖列表

        Args:
            days: 天数，默认7天
            pageIndex: 页码，默认1
            pageSize: 每页条数，默认20

        Returns:
            接口返回数据
        """
        data = {
            "days": days,
            "pageIndex": pageIndex,
            "pageSize": pageSize
        }
        return self.make_request(HOT_ARTICLES_API, data)

    def get_article(self, article_id: str) -> Dict:
        """
        获取帖子详情

        Args:
            article_id: 帖子ID

        Returns:
            接口返回数据
        """
        data = {
            "articleId": article_id
        }
        return self.make_request(VIEW_ARTICLE_API, data)

    def get_replies(self, article_id: str, pageIndex: int = 1, pageSize: int = 20) -> Dict:
        """
        获取回复列表

        Args:
            article_id: 帖子ID
            pageIndex: 页码，默认1
            pageSize: 每页条数，默认20

        Returns:
            接口返回数据
        """
        data = {
            "articleId": article_id,
            "pageIndex": pageIndex,
            "pageSize": pageSize
        }
        return self.make_request(VIEW_REPLIES_API, data)

    def post_thread(self, title: str, content: str) -> tuple:
        """
        发布新帖子

        Args:
            title: 帖子标题
            content: 帖子内容

        Returns:
            (是否成功, 帖子ID或None)
        """
        if not title or not content:
            print("错误：标题和内容不能为空")
            return False, None

        # 构造发帖参数
        post_data = {
            "title": title,
            "content": content
        }

        print(f"正在发布帖子: {title}...")

        result = self.make_request(POST_API, post_data)

        if "error" in result:
            print(f"发帖失败: {result['error']}")
            return False, None

        # 判断成功
        if result.get("success") or result.get("code") == 200 or result.get("status") == "ok":
            print("帖子发布成功！")
            # 提取 ArticleId
            article_id = None
            if isinstance(result.get("data"), dict):
                article_id = result["data"].get("ArticleId")
            elif isinstance(result.get("ArticleId"), (str, int)):
                article_id = result.get("ArticleId")
            return True, article_id
        else:
            print("发帖可能失败，请检查返回信息")
            print(f"返回: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")
            return False, None

    def reply_to_thread(self, article_id: str, content: str) -> tuple:
        """
        回复帖子

        Args:
            article_id: 帖子ID
            content: 回复内容

        Returns:
            (是否成功, 回复ID或None)
        """
        if not article_id or not content:
            print("错误：帖子ID和回复内容不能为空")
            return False, None

        # 构造回帖参数
        reply_data = {
            "articleId": article_id,
            "content": content
        }

        print(f"正在回复帖子 {article_id}...")

        result = self.make_request(REPLY_API, reply_data)

        if "error" in result:
            print(f"回帖失败: {result['error']}")
            return False, None

        # 判断成功
        if result.get("success") or result.get("code") == 200 or result.get("status") == "ok":
            print("回复发布成功！")
            # 提取 CommentId
            reply_id = None
            if isinstance(result.get("data"), dict):
                reply_id = result["data"].get("CommentId") or result["data"].get("Id")
            elif isinstance(result.get("CommentId"), (str, int)):
                reply_id = result.get("CommentId")
            return True, reply_id
        else:
            print("回帖可能失败，请检查返回信息")
            print(f"返回: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")
            return False, None


def main():
    # 加载配置文件
    config = load_config()

    parser = argparse.ArgumentParser(description="东论发帖/回帖工具")
    parser.add_argument("--token", "-k", type=str, help="访问令牌 (优先于配置文件)")
    parser.add_argument("--title", "-t", type=str, help="帖子标题（发帖时必需，可用引号包裹含空格的标题）")
    parser.add_argument("--content", "-c", type=str, help="内容（可用引号包裹含空格的内容，或使用 @文件名 从文件读取）")
    parser.add_argument("--reply", "-r", type=str, help="帖子ID，指定则进行回帖而非发帖")
    parser.add_argument("--save-config", action="store_true", help="保存 token 到配置文件")
    parser.add_argument("--hot", action="store_true", help="获取热帖列表")
    parser.add_argument("--days", "-d", type=int, default=7, help="热帖天数，默认7天")
    parser.add_argument("--page", "-p", type=int, default=1, help="页码，默认1")
    parser.add_argument("--size", "-s", type=int, default=20, help="每页条数，默认20")
    parser.add_argument("--view", "-v", type=str, help="查看帖子详情，参数为帖子ID")
    parser.add_argument("--replies", type=str, help="查看回复列表，参数为帖子ID")

    args = parser.parse_args()

    # 优先使用命令行参数，其次环境变量，最后配置文件
    token = args.token or os.environ.get("CNOOL_API_TOKEN") or config.get("token")

    # 检查必要参数
    if not token:
        parser.print_help()
        print("\n错误：需要提供 token")
        print("方式1: 命令行参数 -k <token>")
        print("方式2: 环境变量 CNOOL_API_TOKEN")
        print("方式3: 配置文件 config.json")
        print("方式4: 首次使用 --save-config 保存 token")
        print(f"\n配置文件路径: {CONFIG_FILE}")
        sys.exit(1)

    # 保存到配置文件（如果指定了 --save-config）
    if args.save_config:
        config["token"] = token
        save_config(config)
        print("配置已保存！")

    # 创建客户端
    client = DonglunAPI(token)

    # 判断是哪种操作模式
    if args.hot:
        # 获取热帖列表
        print(f"正在获取最近 {args.days} 天热帖...")
        result = client.get_hot_articles(days=args.days, pageIndex=args.page, pageSize=args.size)
        if "error" in result:
            print(f"获取热帖失败: {result['error']}")
            sys.exit(1)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)

    if args.view:
        # 查看帖子详情
        print(f"正在查看帖子 {args.view}...")
        result = client.get_article(args.view)
        if "error" in result:
            print(f"查看帖子失败: {result['error']}")
            sys.exit(1)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)

    if args.replies:
        # 查看回复列表
        print(f"正在查看帖子 {args.replies} 的回复...")
        result = client.get_replies(args.replies, pageIndex=args.page, pageSize=args.size)
        if "error" in result:
            print(f"查看回复失败: {result['error']}")
            sys.exit(1)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)

    # 发帖/回帖模式需要 content 参数
    if not args.content:
        parser.print_help()
        print("\n错误：发帖/回帖时需要提供内容 (-c)")
        sys.exit(1)

    # 处理内容参数：如果以 @ 开头，从文件读取
    content = args.content
    if content.startswith('@') and len(content) > 1:
        file_path = content[1:]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"已从文件 {file_path} 读取内容")
        except Exception as e:
            print(f"读取文件失败: {e}")
            sys.exit(1)

    # 判断是发帖还是回帖
    if args.reply:
        # 回帖模式
        success, reply_id = client.reply_to_thread(args.reply, content)
        if success and reply_id:
            print(f"回复ID: {reply_id}")
    else:
        # 发帖模式
        if not args.title:
            parser.print_help()
            print("\n错误：发帖时需要提供标题 (-t)")
            sys.exit(1)

        success, article_id = client.post_thread(args.title, content)

        # 显示帖子链接
        if success and article_id:
            print(f"帖子ID: {article_id}")
            print(f"帖子链接: https://bbs.cnool.net/{article_id}.html")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
