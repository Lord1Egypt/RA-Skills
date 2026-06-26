import requests

class FeishuSkill:
    def __init__(self, config):
        # 从配置里读取，不写死
        self.app_id = config["APP_ID"]
        self.app_secret = config["APP_SECRET"]
        self.default_receive_id = config.get("DEFAULT_RECEIVE_ID", "")

    def get_tenant_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        resp = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })
        return resp.json().get("tenant_access_token")

    def send_msg(self, receive_id, text):
        token = self.get_tenant_token()
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "receive_id": receive_id,
            "msg_type": "text",
            "content": f'{{"text":"{text}"}}'
        }
        return requests.post(url, headers=headers, json=data).json()

# OpenClaw 固定入口
def run(config, params):
    skill = FeishuSkill(config)
    receive_id = params.get("receive_id", skill.default_receive_id)
    return skill.send_msg(receive_id, params["text"])