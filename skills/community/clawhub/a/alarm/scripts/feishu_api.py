from __future__ import annotations

import json
import requests

from config import get_optional, get_required


class FeishuClient:
    def __init__(self) -> None:
        self.base_url = get_optional('FEISHU_BASE_URL', 'https://open.feishu.cn')
        self.app_id = get_required('FEISHU_APP_ID')
        self.app_secret = get_required('FEISHU_APP_SECRET')

    def tenant_access_token(self) -> str:
        resp = requests.post(
            f'{self.base_url}/open-apis/auth/v3/tenant_access_token/internal',
            headers={'Content-Type': 'application/json; charset=utf-8'},
            json={'app_id': self.app_id, 'app_secret': self.app_secret},
            timeout=30,
        )
        body = resp.json()
        if not resp.ok or body.get('code', 0) != 0:
            raise RuntimeError(f'飞书获取 tenant_access_token 失败: {body}')
        token = (body.get('tenant_access_token') or '').strip()
        if not token:
            raise RuntimeError(f'飞书 tenant_access_token 为空: {body}')
        return token

    def send_text_message(self, receive_id: str, text: str, receive_id_type: str = 'chat_id') -> dict:
        token = self.tenant_access_token()
        resp = requests.post(
            f'{self.base_url}/open-apis/im/v1/messages',
            params={'receive_id_type': receive_id_type},
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json; charset=utf-8',
            },
            json={
                'receive_id': receive_id,
                'msg_type': 'text',
                'content': json.dumps({'text': text}, ensure_ascii=False),
            },
            timeout=30,
        )
        body = resp.json()
        if not resp.ok or body.get('code', 0) != 0:
            raise RuntimeError(f'飞书发送文本消息失败: status={resp.status_code}, body={body}')
        return body
