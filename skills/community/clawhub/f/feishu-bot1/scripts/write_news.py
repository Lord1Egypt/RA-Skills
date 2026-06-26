import json, urllib.request, urllib.error

config = json.load(open('C:/Users/10430/.openclaw/workspace/skills/feishu-ops/scripts/config.json'))
token = 't-g1043jexJNXU6IOGYC26VWSWESLRGIMMOWRXJWYS'
doc_token = 'KH6qdDlNuoACh4xSaPTcFFr3npc'

# get root block id
url = 'https://open.feishu.cn/open-apis/docx/v1/documents/' + doc_token + '/blocks?page_size=50'
req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + token})
with urllib.request.urlopen(req) as r:
    result = json.loads(r.read())

root_id = result['data']['items'][0]['block_id']
print('root block:', root_id)

def h1(content):
    return {'block_type': 3, 'heading1': {'elements': [{'type': 'text_run', 'text_run': {'content': content}}]}}

def h2(content):
    return {'block_type': 4, 'heading2': {'elements': [{'type': 'text_run', 'text_run': {'content': content}}]}}

def bullet(content):
    return {'block_type': 12, 'bullet': {'elements': [{'type': 'text_run', 'text_run': {'content': content}}]}}

def ordered(content):
    return {'block_type': 13, 'ordered': {'elements': [{'type': 'text_run', 'text_run': {'content': content}}]}}

def text(content):
    return {'block_type': 2, 'text': {'elements': [{'type': 'text_run', 'text_run': {'content': content}}]}}

news = [
    h1('今日热点新闻汇总'),
    h2('国内要闻'),
    bullet('一批重大工程紧锣密鼓，奏响"春日奋进曲"'),
    bullet('王毅表示：这场战争本不该发生，更没必要再打下去'),
    bullet('"投资者保护"首次写入十五五，证监会火速部署清除"拦路虎"'),
    bullet('商办最低首付调至3成，北上广杭蓉锁定一线城市'),
    bullet('多地宣布27年缩减中考计分科目'),
    h2('国际热点'),
    bullet('伊朗外长怒斥以色列"暗杀常态化"，称国际社会不应"双标"'),
    bullet('美媒：世卫组织官员正为中东地区可能发生的"核灾难"做准备'),
    bullet('牛弹琴：重大转折点，战争进入疯狂阶段'),
    bullet('中国代表：中东局势正被推向危险深渊'),
    h2('科技财经'),
    bullet('Agent推高需求，全球云计算巨头集体涨价'),
    bullet('腾讯2025年营收增长14%，今年AI新产品投入至少翻倍'),
    bullet('苹果CEO库克现身成都，锚定中国供应链'),
    bullet('金价大跌，市民排队买金（现货黄金跌破4900美元关口）'),
    h2('社会民生'),
    bullet('前中超球员邱忠辉：送外卖不丢人，凭劳动挣钱最光荣'),
    bullet('央媒：是时候打破眼镜行业的价格"滤镜"了'),
    bullet('胖东来169元1克拉方糖戒指再上架，每人限购5枚'),
    h2('体育速递'),
    bullet('唐钱婷刷新50蛙亚洲纪录（预赛29秒49）'),
    bullet('东契奇&库里膝盖出血：地板擦伤留下的真实血迹'),
    text('—— 以上新闻整理自新浪网，采集时间：2026年3月19日'),
]

url2 = 'https://open.feishu.cn/open-apis/docx/v1/documents/' + doc_token + '/blocks/' + root_id + '/children'
data = json.dumps({'children': news}).encode('utf-8')
req2 = urllib.request.Request(url2, data=data, method='POST', headers={'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer ' + token})
try:
    with urllib.request.urlopen(req2) as r:
        result2 = json.loads(r.read())
    code = result2.get('code')
    children = result2.get('data', {}).get('children', [])
    print('code:', code, '| children count:', len(children))
    if code != 0:
        print('msg:', result2.get('msg'))
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print('HTTP Error:', e.code)
    print('Body:', body[:500])
