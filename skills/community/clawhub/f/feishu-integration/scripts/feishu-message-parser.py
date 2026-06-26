#!/usr/bin/env python3
"""
飞书消息解析器
支持富文本、引用消息、图片OCR识别
"""

import json
import os
import sys
import requests
from typing import Dict, List, Optional


class FeishuMessageParser:
    """飞书消息统一解析类"""
    
    def __init__(self, tenant_token: str):
        self.tenant_token = tenant_token
        self.base_url = "https://open.feishu.cn/open-apis"
    
    def parse(self, message_data: Dict) -> str:
        """
        统一解析入口
        
        Args:
            message_data: 飞书消息数据
            
        Returns:
            解析后的纯文本内容
        """
        msg_type = message_data.get("msg_type")
        
        parsers = {
            "text": self._parse_text,
            "post": self._parse_post,
            "interactive": self._parse_card,
            "image": self._parse_image,
        }
        
        parser = parsers.get(msg_type, lambda x: "[不支持的消息类型]")
        return parser(message_data)
    
    def _parse_text(self, data: Dict) -> str:
        """解析纯文本消息"""
        try:
            content = json.loads(data.get("body", {}).get("content", "{}"))
            text = content.get("text", "")
            
            # 处理引用消息
            quoted = data.get("quoted_message_content")
            if quoted:
                return f"【引用】{quoted}\n【回复】{text}"
            
            return text
        except Exception as e:
            return f"[文本解析失败: {e}]"
    
    def _parse_post(self, data: Dict) -> str:
        """解析富文本消息（post 类型）"""
        try:
            content = json.loads(data.get("body", {}).get("content", "{}"))
            return self.parse_rich_text(content)
        except Exception as e:
            return f"[富文本解析失败: {e}]"
    
    def parse_rich_text(self, content: Dict, return_structured: bool = False) -> str:
        """
        解析飞书富文本内容
        
        支持的标签：
        - text: 纯文本
        - lark_md: Markdown 内容
        - at: @提及
        - a: 链接
        - img: 图片
        
        Args:
            content: 富文本内容
            return_structured: 是否返回结构化数据
        """
        if isinstance(content, str):
            content = json.loads(content)
        
        result = []
        structured_data = {
            "title": "",
            "text_content": [],
            "images": [],
            "mentions": [],
            "links": []
        }
        
        # 处理标题
        title = content.get("title")
        if title:
            result.append(f"# {title}\n")
            structured_data["title"] = title
        
        # 处理内容块（支持 content 和 elements 两种格式）
        content_blocks = content.get("content") or content.get("elements") or []
        for row in content_blocks:
            line = []
            for element in row:
                tag = element.get("tag")
                
                if tag == "text":
                    text = element.get("text", "")
                    line.append(text)
                    structured_data["text_content"].append(text)
                
                elif tag == "lark_md":
                    md_content = element.get("content", "")
                    line.append(md_content)
                    structured_data["text_content"].append(md_content)
                
                elif tag == "at":
                    user_name = element.get("user_name", "某人")
                    user_id = element.get("user_id", "")
                    line.append(f"@{user_name}")
                    structured_data["mentions"].append({
                        "id": user_id,
                        "name": user_name
                    })
                
                elif tag == "a":
                    text = element.get("text", "")
                    href = element.get("href", "")
                    line.append(f"[{text}]({href})" if text else href)
                    structured_data["links"].append({
                        "text": text,
                        "url": href
                    })
                
                elif tag == "img":
                    image_key = element.get("image_key", "")
                    line.append(f"[图片:{image_key}]")
                    structured_data["images"].append(image_key)
            
            result.append("".join(line))
        
        if return_structured:
            structured_data["text_content"] = "\n".join(structured_data["text_content"])
            structured_data["markdown_content"] = "\n".join(result)
            return structured_data
        
        return "\n".join(result)
    
    def _parse_card(self, data: Dict) -> str:
        """解析交互式卡片消息"""
        try:
            content = json.loads(data.get("body", {}).get("content", "{}"))
            texts = []
            
            # 提取标题
            if content.get("title"):
                texts.append(f"# {content['title']}")
            
            # 提取内容
            for row in content.get("content", []):
                for elem in row:
                    if elem.get("tag") in ["text", "lark_md"]:
                        texts.append(elem.get("content", elem.get("text", "")))
            
            return "\n".join(texts)
        except Exception as e:
            return f"[卡片解析失败: {e}]"
    
    def _parse_image(self, data: Dict) -> str:
        """解析图片消息（支持 OCR）"""
        try:
            content = json.loads(data.get("body", {}).get("content", "{}"))
            image_key = content.get("image_key")
            
            if not image_key:
                return "[图片，无key]"
            
            # 尝试 OCR 识别
            try:
                text = self.get_image_text(image_key)
                return f"[图片]: {text}" if text else "[图片，无文字]"
            except Exception as e:
                return f"[图片:{image_key}]"
        except Exception as e:
            return f"[图片解析失败: {e}]"
    
    def get_image_text(self, image_key: str) -> str:
        """
        使用飞书 OCR API 识别图片文字
        
        Args:
            image_key: 图片 key
            
        Returns:
            识别出的文字内容
        """
        url = f"{self.base_url}/optical-char-recognition/v1/image/recognize_basic"
        headers = {
            "Authorization": f"Bearer {self.tenant_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json={"image_key": image_key})
        result = response.json()
        
        if result.get("code") == 0:
            texts = result.get("data", {}).get("texts", [])
            return "\n".join([t.get("text", "") for t in texts])
        
        return ""
    
    def parse_quoted_message(self, message_data: Dict) -> str:
        """
        解析引用回复消息
        
        Args:
            message_data: 消息数据
            
        Returns:
            格式化的引用+回复内容
        """
        try:
            content = json.loads(message_data.get("body", {}).get("content", "{}"))
            current_text = content.get("text", "")
            quoted_content = message_data.get("quoted_message_content", "")
            
            if quoted_content:
                return f"【引用】{quoted_content}\n【回复】{current_text}"
            
            return current_text
        except Exception as e:
            return f"[引用解析失败: {e}]"


def main():
    """命令行入口"""
    import argparse
    
    parser_cli = argparse.ArgumentParser(description="飞书消息解析器")
    parser_cli.add_argument("tenant_token", help="Tenant access token")
    parser_cli.add_argument("message_json", help="消息 JSON 字符串")
    parser_cli.add_argument("--format", choices=["text", "json"], default="text",
                           help="输出格式：text (纯文本) 或 json (结构化)")
    
    args = parser_cli.parse_args()
    
    try:
        message_data = json.loads(args.message_json)
        parser = FeishuMessageParser(args.tenant_token)
        
        if args.format == "json":
            # 返回结构化数据
            msg_type = message_data.get("msg_type")
            if msg_type in ["post", "interactive"]:
                content = json.loads(message_data.get("body", {}).get("content", "{}"))
                result = parser.parse_rich_text(content, return_structured=True)
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                # 其他类型暂不支持结构化输出
                result = parser.parse(message_data)
                print(json.dumps({"text": result}, ensure_ascii=False, indent=2))
        else:
            # 返回纯文本
            result = parser.parse(message_data)
            print(result)
    except Exception as e:
        print(f"解析失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
