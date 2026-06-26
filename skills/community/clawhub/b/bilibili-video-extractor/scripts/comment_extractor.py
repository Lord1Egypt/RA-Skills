#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
B站评论提取器
获取视频的热门评论和评论分析
"""

import argparse
import json
import sys
import time
from typing import List, Dict, Any, Optional
import requests


class CommentExtractor:
    """B站评论提取器"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.bilibili.com"
        })

    def get_video_aid(self, bvid: str) -> Optional[int]:
        """获取视频aid"""
        try:
            url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
            response = self.session.get(url, timeout=10)
            data = response.json()
            if data.get("code") == 0:
                return data["data"]["aid"]
        except Exception:
            pass
        return None

    def get_comments(self, oid: int, mode: int = 3, limit: int = 50,
                     sort: str = "hot") -> List[Dict]:
        """获取评论

        Args:
            oid: 视频aid
            mode: 排序模式 (2=最新, 3=最热)
            limit: 获取数量
            sort: 排序方式 hot/time
        """
        mode = 2 if sort == "time" else 3

        comments = []
        pn = 1

        while len(comments) < limit:
            url = f"https://api.bilibili.com/x/v2/reply"
            params = {
                "type": 1,
                "oid": oid,
                "mode": mode,
                "ps": min(limit, 20),
                "pn": pn
            }

            try:
                response = self.session.get(url, params=params, timeout=10)
                data = response.json()

                if data.get("code") != 0:
                    break

                replies = data.get("data", {}).get("replies", []) or []
                if not replies:
                    break

                for reply in replies:
                    comments.append(self._format_comment(reply))

                    # 获取子回复
                    if reply.get("rcount", 0) > 0:
                        sub_replies = self._get_sub_replies(reply.get("rpid"))
                        comments.extend(sub_replies)

                pn += 1
                time.sleep(0.3)

            except Exception as e:
                print(f"[警告] 获取评论失败: {e}", file=sys.stderr)
                break

        return comments[:limit]

    def _get_sub_replies(self, rpid: int) -> List[Dict]:
        """获取子回复"""
        try:
            url = f"https://api.bilibili.com/x/v2/reply/reply"
            params = {
                "type": 1,
                "oid": rpid,
                "pn": 1,
                "ps": 3
            }
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()

            if data.get("code") == 0:
                replies = data.get("data", {}).get("replies", []) or []
                return [self._format_comment(r) for r in replies[:3]]
        except Exception:
            pass
        return []

    def _format_comment(self, reply: Dict) -> Dict:
        """格式化评论数据"""
        return {
            "rpid": reply.get("rpid"),
            "uid": reply.get("member", {}).get("uname", ""),
            "content": reply.get("content", {}).get("message", ""),
            "like": reply.get("like", 0),
            "ctime": reply.get("ctime", 0),
            "reply_count": reply.get("rcount", 0),
            "dynamic_id": reply.get("dynamic_id_str", "")
        }

    def analyze_comments(self, comments: List[Dict]) -> Dict[str, Any]:
        """分析评论"""
        if not comments:
            return {"error": "无评论数据"}

        total = len(comments)
        total_likes = sum(c.get("like", 0) for c in comments)

        # 热门评论
        hot_comments = sorted(comments, key=lambda x: x.get("like", 0), reverse=True)[:10]

        # 提取关键词（简单统计）
        all_text = " ".join(c.get("content", "") for c in comments)
        words = self._extract_keywords(all_text)

        # 评论长度分析
        lengths = [len(c.get("content", "")) for c in comments]
        avg_length = sum(lengths) / len(lengths) if lengths else 0

        return {
            "summary": {
                "total_comments": total,
                "total_likes": total_likes,
                "avg_likes": round(total_likes / total, 1) if total else 0,
                "avg_length": round(avg_length, 1)
            },
            "hot_comments": hot_comments,
            "keywords": words,
            "sentiment": self._analyze_sentiment(all_text)
        }

    def _extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
        """简单关键词提取（基于词频）"""
        # 常见停用词
        stopwords = {
            "的", "了", "是", "我", "你", "他", "她", "它", "们", "这", "那",
            "个", "在", "有", "和", "就", "不", "人", "都", "一", "一个",
            "上", "也", "很", "到", "说", "要", "去", "你", "你", "会",
            "可以", "没有", "什么", "怎么", "为什么", "这个", "那个"
        }

        # 简单分词（按空格和标点）
        import re
        words = re.findall(r'[\u4e00-\u9fa5]+', text)

        # 统计词频
        freq = {}
        for word in words:
            if len(word) >= 2 and word not in stopwords:
                freq[word] = freq.get(word, 0) + 1

        # 排序返回
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [w[0] for w in sorted_words[:top_n]]

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """简单情感分析"""
        positive = ["赞", "好", "棒", "厉害", "支持", "喜欢", "牛", "强", "顶", "顶"]
        negative = ["差", "烂", "垃圾", "坑", "骗", "难看", "无语", "吐槽", "失望"]

        pos_count = sum(1 for w in positive if w in text)
        neg_count = sum(1 for w in negative if w in text)

        if pos_count > neg_count:
            sentiment = "正面"
        elif neg_count > pos_count:
            sentiment = "负面"
        else:
            sentiment = "中性"

        return {
            "倾向": sentiment,
            "正面词频": pos_count,
            "负面词频": neg_count
        }


def main():
    parser = argparse.ArgumentParser(description="B站评论提取工具")
    parser.add_argument("--bvid", required=True, help="视频BV号")
    parser.add_argument("--limit", type=int, default=50, help="获取数量")
    parser.add_argument("--sort", choices=["hot", "time"], default="hot",
                        help="排序方式: hot(热门) / time(最新)")
    parser.add_argument("--output", "-o", help="输出文件路径")

    args = parser.parse_args()

    extractor = CommentExtractor()

    # 获取aid
    print(f"[信息] 获取视频信息: {args.bvid}")
    aid = extractor.get_video_aid(args.bvid)

    if not aid:
        print("[错误] 无法获取视频信息")
        sys.exit(1)

    print(f"[信息] 开始获取评论 (模式: {args.sort})")
    comments = extractor.get_comments(aid, limit=args.limit, sort=args.sort)

    print(f"[信息] 获取到 {len(comments)} 条评论")

    # 分析
    analysis = extractor.analyze_comments(comments)

    # 输出
    result = {
        "bvid": args.bvid,
        "aid": aid,
        "comments": comments,
        "analysis": analysis
    }

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[保存] 已保存至: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
