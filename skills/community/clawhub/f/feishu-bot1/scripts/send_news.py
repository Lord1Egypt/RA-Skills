import json, urllib.request, uuid

config = json.load(open('C:/Users/10430/.openclaw/workspace/skills/feishu-ops/scripts/config.json', encoding='utf-8'))
url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
data = json.dumps({'app_id': config['app_id'], 'app_secret': config['app_secret']}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as r:
    token = json.loads(r.read())['tenant_access_token']

news = """以下是今日国际热点新闻 Top 10（2026年3月19日）：

1. 中美巴黎经贸磋商释放积极信号，美方希望双边关系稳定发展
2. 以军称伊朗使用集束弹头导弹再次发动袭击，中东局势持续升级
3. 美情报总监称伊朗政权"完整但遭严重削弱"
4. 美军多处基地遭袭击，"被炸了个遍"
5. 世卫组织正为中东地区可能发生的"核灾难"做准备
6. 日本央行维持政策利率在0.75%左右
7. 卡塔尔多处能源设施再遭袭起火，阿联酋谴责
8. 一艘船在阿联酋海域遭袭起火，波斯湾局势紧张
9. 美联储按兵不动，美元大涨，人民币对美元汇率跌破6.9
10. 高市启"跪美"外交，引发国际关注

—— 由AI龙虾自动整理推送"""

url2 = 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id'
payload = {
    'receive_id': 'oc_2c6df8f6e06e88d34729baacc124b89e',
    'msg_type': 'text',
    'content': json.dumps({'text': news}),
    'uuid': str(uuid.uuid4())
}
data2 = json.dumps(payload).encode('utf-8')
req2 = urllib.request.Request(url2, data=data2, method='POST', headers={'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer ' + token})
with urllib.request.urlopen(req2) as r:
    result = json.loads(r.read())
print('code:', result.get('code'), '| msg:', result.get('msg'))
