#!/usr/bin/env python3
"""Feishu Sheets Enhanced - 飞书表格增强"""

import requests
import json


class FeishuSheetsEnhanced:
    """飞书表格增强功能"""
    
    def __init__(self, app_id=None, app_secret=None):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
    
    def get_access_token(self):
        """获取Access Token"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        resp = requests.post(url, json=data)
        if resp.status_code == 200:
            self.access_token = resp.json().get("tenant_access_token")
            return self.access_token
        return None
    
    def get_spreadsheet(self, spreadsheet_token):
        """获取表格元信息"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        resp = requests.get(url, headers=headers)
        return resp.json()
    
    def get_sheet_meta(self, spreadsheet_token, sheet_id):
        """获取Sheet元信息"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheet/{sheet_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        resp = requests.get(url, headers=headers)
        return resp.json()
    
    def add_sheet(self, spreadsheet_token, title):
        """添加Sheet"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheets"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {"properties": [{"title": title}]}
        resp = requests.post(url, json=data, headers=headers)
        return resp.json()
    
    def copy_sheet(self, spreadsheet_token, sheet_id, new_title):
        """复制Sheet"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheets/copy"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {"sheet": {"sheet_id": sheet_id, "title": new_title}}
        resp = requests.post(url, json=data, headers=headers)
        return resp.json()
    
    def delete_sheet(self, spreadsheet_token, sheet_id):
        """删除Sheet"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheets/{sheet_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        resp = requests.delete(url, headers=headers)
        return resp.json()
    
    def insert_dimension(self, spreadsheet_token, sheet_id, dimension, start_index, end_index):
        """插入行或列"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheets/{sheet_id}/insert_dimension"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {
            "dimension": dimension,
            "start_index": start_index,
            "end_index": end_index
        }
        resp = requests.post(url, json=data, headers=headers)
        return resp.json()
    
    def delete_dimension(self, spreadsheet_token, sheet_id, dimension, start_index, end_index):
        """删除行或列"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheets/{sheet_id}/delete_dimension"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {
            "dimension": dimension,
            "start_index": start_index,
            "end_index": end_index
        }
        resp = requests.post(url, json=data, headers=headers)
        return resp.json()
    
    def set_style(self, spreadsheet_token, sheet_id, range, style):
        """设置样式"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheets/{sheet_id}/style"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {"range": range, "style": style}
        resp = requests.put(url, json=data, headers=headers)
        return resp.json()
    
    def protect_sheet(self, spreadsheet_token, sheet_id, permission):
        """保护Sheet"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheets/{sheet_id}/protection"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {"permission": permission}
        resp = requests.put(url, json=data, headers=headers)
        return resp.json()
    
    def find_replace(self, spreadsheet_token, sheet_id, find, replace, match_case=False):
        """查找替换"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheets/{sheet_id}/find_replace"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {
            "find": find,
            "replacement": replace,
            "match_case": match_case
        }
        resp = requests.post(url, json=data, headers=headers)
        return resp.json()
    
    def create_condition_format(self, spreadsheet_token, sheet_id, range, condition):
        """创建条件格式"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheets/{sheet_id}/conditional_format"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {"range": range, "condition": condition}
        resp = requests.post(url, json=data, headers=headers)
        return resp.json()
    
    def get_comments(self, spreadsheet_token, sheet_id):
        """获取评论"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheets/{sheet_id}/comments"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        resp = requests.get(url, headers=headers)
        return resp.json()
    
    def add_comment(self, spreadsheet_token, sheet_id, cell, content):
        """添加评论"""
        url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheet/{spreadsheet_token}/sheets/{sheet_id}/comments"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {"cell": cell, "message": content}
        resp = requests.post(url, json=data, headers=headers)
        return resp.json()


if __name__ == "__main__":
    print("Feishu Sheets Enhanced loaded")