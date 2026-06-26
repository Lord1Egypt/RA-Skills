import requests
import json
from src.config import FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_BASE_URL

class FeishuClient:
    def __init__(self):
        self.app_id = FEISHU_APP_ID
        self.app_secret = FEISHU_APP_SECRET
        self.base_url = FEISHU_BASE_URL
        self.token = None
        
        if not self.app_id or not self.app_secret:
            raise ValueError(
                "❌ 未找到飞书 App ID 或 Secret！\n"
                "请您先前往飞书开放平台 (https://open.feishu.cn/app/) 创建一个企业自建应用。\n"
                "创建后，将获取到的 App ID 和 App Secret 填入 .env 文件或作为环境变量传入。"
            )

    def get_tenant_access_token(self):
        """获取 tenant_access_token"""
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("code") != 0:
                raise Exception(f"Failed to get token: {data}")
            self.token = data.get("tenant_access_token")
            return self.token
        except Exception as e:
            print(f"Error getting token: {e}")
            raise

    def _get_headers(self):
        if not self.token:
            self.get_tenant_access_token()
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def get_comments(self, document_token, page_token=None):
        """
        获取评论列表
        文档中提到: GET /comment/v1/comments
        实际使用: GET /drive/v1/files/:file_token/comments
        为了兼容性，我们优先使用 drive 接口，因为它是处理 docx 评论的标准方式。
        """
        url = f"{self.base_url}/drive/v1/files/{document_token}/comments"
        params = {
            "file_type": "docx",
            "page_size": 20
        }
        if page_token:
            params["page_token"] = page_token
            
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting comments: {e}")
            return None

    def get_block(self, document_id, block_id):
        """
        获取块内容
        GET /docx/v1/documents/{document_id}/blocks/{block_id}
        """
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{block_id}"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting block {block_id}: {e}")
            return None

    def update_block(self, document_id, block_id, new_text_content):
        """
        更新块内容
        PATCH /docx/v1/documents/{document_id}/blocks/{block_id}
        
        Args:
            document_id: 文档 ID
            block_id: 块 ID
            new_text_content: 新的文本内容
            
        Returns:
            dict: API 响应结果
        """
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{block_id}"
        
        payload = {
            "update_text_elements": {
                "elements": [
                    {
                        "text_run": {
                            "content": new_text_content,
                            "text_element_style": {}
                        }
                    }
                ]
            }
        }
        
        try:
            response = requests.patch(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error updating block {block_id}: {e}")
            return None

    def delete_block(self, document_id, block_id):
        """
        删除块内容（通过清空内容实现）
        
        注意：飞书 docx API 没有直接的 DELETE /blocks/{block_id} 接口。
        实际做法是用 PATCH 更新块，将内容设置为空字符串。
        
        Args:
            document_id: 文档 ID
            block_id: 块 ID
            
        Returns:
            dict: API 响应结果，{"ok": True, "block_id": "..."} 或 {"ok": False, "error": "..."}
        """
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{block_id}"
        
        payload = {
            "update_text_elements": {
                "elements": [
                    {
                        "text_run": {
                            "content": "",
                            "text_element_style": {}
                        }
                    }
                ]
            }
        }
        
        try:
            response = requests.patch(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            result = response.json()
            if result.get("code") == 0:
                return {"ok": True, "block_id": block_id, "message": "块内容已清空"}
            else:
                return {"ok": False, "error": result.get("msg", "unknown_error")}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_text_from_block(self, document_id, block_id, text_to_delete):
        """
        从块中删除指定的文本（只删除选中的部分，保留其他内容）
        
        Args:
            document_id: 文档 ID
            block_id: 块 ID
            text_to_delete: 要删除的文本内容
            
        Returns:
            dict: API 响应结果，{"ok": True, "new_content": "..."} 或 {"ok": False, "error": "..."}
        """
        # 首先获取块的当前内容
        block_data = self.get_block(document_id, block_id)
        if not block_data or block_data.get("code") != 0:
            return {"ok": False, "error": "无法获取块内容"}
        
        block = block_data.get("data", {}).get("block", {})
        text_elements = block.get("text", {}).get("elements", [])
        
        # 拼接当前所有内容
        current_content = ""
        for elem in text_elements:
            current_content += elem.get("text_run", {}).get("content", "")
        
        # 删除指定的文本
        if text_to_delete in current_content:
            new_content = current_content.replace(text_to_delete, "", 1)
        else:
            # 如果找不到完全匹配，尝试模糊匹配（去掉首尾空格后匹配）
            text_to_delete = text_to_delete.strip()
            if text_to_delete in current_content:
                new_content = current_content.replace(text_to_delete, "", 1)
            else:
                return {"ok": False, "error": "未找到要删除的文本内容"}
        
        # 更新块
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{block_id}"
        
        payload = {
            "update_text_elements": {
                "elements": [
                    {
                        "text_run": {
                            "content": new_content,
                            "text_element_style": {}
                        }
                    }
                ]
            }
        }
        
        try:
            response = requests.patch(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            result = response.json()
            if result.get("code") == 0:
                return {"ok": True, "new_content": new_content, "message": "文本已删除"}
            else:
                return {"ok": False, "error": result.get("msg", "unknown_error")}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def reply_comment(self, file_token, comment_id, content):
        """
        回复评论
        POST /drive/v1/files/:file_token/comments/:comment_id/replies
        
        Args:
            file_token: 文档 token
            comment_id: 评论 ID
            content: 回复内容（纯文本）
            
        Returns:
            dict: API 响应结果
        """
        url = f"{self.base_url}/drive/v1/files/{file_token}/comments/{comment_id}/replies"
        params = {"file_type": "docx"}
        payload = {
            "content": {
                "elements": [
                    {
                        "text_run": {
                            "text": content
                        },
                        "type": "text_run"
                    }
                ]
            }
        }
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error replying comment {comment_id}: {e}")
            return None

    def resolve_comment(self, file_token, comment_id):
        """
        标记评论为已解决
        PATCH /drive/v1/files/:file_token/comments/:comment_id
        
        注意：必须使用 PATCH 方法，PUT 会返回 404
        
        Args:
            file_token: 文档 token
            comment_id: 评论 ID
            
        Returns:
            dict: API 响应结果
        """
        url = f"{self.base_url}/drive/v1/files/{file_token}/comments/{comment_id}"
        params = {"file_type": "docx"}
        payload = {
            "is_solved": True
        }
        try:
            response = requests.patch(url, headers=self._get_headers(), json=payload, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error resolving comment {comment_id}: {e}")
            return None
    
    def export_markdown(self, document_id):
        """
        导出 MD (备份)
        GET /docx/v1/documents/{token}/export_markdown (需求文档路径)
        真实 API 可能是异步任务，或者直接下载。
        我们先按文档写。
        """
        url = f"{self.base_url}/docx/v1/documents/{document_id}/export_markdown"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error exporting markdown for document {document_id}: {e}")
            return None

    def insert_blocks(self, document_id, blocks, anchor_block_id=None, before=True):
        """
        插入块到文档
        POST /docx/v1/documents/{document_id}/blocks
        
        Args:
            document_id: 文档 ID
            blocks: 要插入的块列表
            anchor_block_id: 锚点块 ID（可选，不传则添加到文档末尾）
            before: 是否在锚点块之前插入（默认 True）
        """
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks"
        
        payload = {
            "blocks": blocks
        }
        
        if anchor_block_id:
            payload["anchor_block_id"] = anchor_block_id
            payload["before"] = before
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            print(f"Insert blocks status: {response.status_code}")
            print(f"Insert blocks response: {response.text[:500]}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error inserting blocks: {e}")
            return None

    def add_text_to_document_start(self, document_id, text_content, bold=False):
        """
        在文档开头添加文本块
        
        Args:
            document_id: 文档 ID
            text_content: 文本内容
            bold: 是否加粗
        """
        # 首先获取文档的第一个块作为锚点
        blocks_data = self.get_blocks(document_id)
        if not blocks_data or "data" not in blocks_data:
            print("Failed to get document blocks")
            return None
        
        blocks = blocks_data.get("data", {}).get("blocks", [])
        if not blocks:
            print("No blocks found in document")
            return None
        
        # 找到第一个根级别的块
        anchor_block = None
        for block in blocks:
            if block.get("parent_id") == document_id:
                anchor_block = block
                break
        
        if not anchor_block:
            print("No root-level block found")
            return None
        
        # 创建要插入的文本块
        new_blocks = [
            {
                "block_type": 2,
                "text": {
                    "elements": [
                        {
                            "text_run": {
                                "content": text_content,
                                "text_element_style": {
                                    "bold": bold
                                }
                            }
                        }
                    ],
                    "style": {
                        "align": 1
                    }
                }
            }
        ]
        
        # 在第一个块之前插入
        return self.insert_blocks(
            document_id,
            new_blocks,
            anchor_block_id=anchor_block["block_id"],
            before=True
        )

    def get_blocks(self, document_id, page_token=None):
        """
        获取文档块列表
        GET /docx/v1/documents/{document_id}/blocks
        
        返回格式：{"code": 0, "data": {"items": [...], "has_more": bool, "page_token": str}}
        """
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks"
        params = {}
        if page_token:
            params["page_token"] = page_token
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            result = response.json()
            # 飞书 API 返回 items 而不是 blocks
            if "data" in result and "items" in result["data"]:
                result["data"]["blocks"] = result["data"]["items"]
            return result
        except Exception as e:
            print(f"Error getting blocks: {e}")
            return None

    def prepend_summary_to_document(self, document_id, summary_text):
        """
        在文档开头添加摘要（通过修改第一个块实现）
        
        Args:
            document_id: 文档 ID
            summary_text: 摘要文本内容
            
        Returns:
            dict: API 响应结果
        """
        # 获取文档的第一个块
        blocks_data = self.get_blocks(document_id)
        if not blocks_data or "data" not in blocks_data:
            return {"ok": False, "error": "failed_to_fetch_blocks"}
        
        blocks = blocks_data.get("data", {}).get("blocks", [])
        if not blocks:
            return {"ok": False, "error": "no_blocks_found"}
        
        # 获取第一个块（通常是标题）
        first_block = blocks[0]
        first_block_id = first_block["block_id"]
        block_type = first_block["block_type"]
        
        # 获取原始内容
        original_content = ""
        if block_type == 1:  # heading1
            original_content = first_block.get("heading1", {}).get("elements", [{}])[0].get("text_run", {}).get("content", "")
        elif block_type == 3:  # heading2
            original_content = first_block.get("heading2", {}).get("elements", [{}])[0].get("text_run", {}).get("content", "")
        elif block_type == 4:  # heading3
            original_content = first_block.get("heading3", {}).get("elements", [{}])[0].get("text_run", {}).get("content", "")
        elif block_type == 2:  # text
            original_content = first_block.get("text", {}).get("elements", [{}])[0].get("text_run", {}).get("content", "")
        
        # 构建新内容：摘要 + 分隔线 + 原始内容
        new_content = f"{summary_text}\n\n────────────────────────────────────────\n\n{original_content}"
        
        # 更新块
        url = f"{self.base_url}/docx/v1/documents/{document_id}/blocks/{first_block_id}"
        payload = {
            "update_text_elements": {
                "elements": [
                    {
                        "text_run": {
                            "content": new_content,
                            "text_element_style": {}
                        }
                    }
                ]
            }
        }
        
        try:
            response = requests.patch(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            result = response.json()
            if result.get("code") == 0:
                return {"ok": True, "block_id": first_block_id, "message": "摘要已成功添加到文档开头"}
            else:
                return {"ok": False, "error": result.get("msg", "unknown_error")}
        except Exception as e:
            return {"ok": False, "error": str(e)}
