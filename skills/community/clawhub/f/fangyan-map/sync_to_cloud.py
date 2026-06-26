#!/usr/bin/env python3
"""
同步生词到云端共享 bitable

支持所有11种方言自动写入云端。

使用方法：
    python3 sync_to_cloud.py <普通话> <方言词> [方言区] [词性] [备注]
    python3 sync_to_cloud.py "漂亮" "得劲儿" "哈尔滨话" "形容词" "形容很舒服"
    python3 sync_to_cloud.py "聊天" "倾偈" "广东话" "日常用语" "粤语日常表达"

前提：
    写入 bitable 需要有对应权限（徐哥在飞书里给虾加权限后可用）
"""

import sys
import os
import json
import urllib.request
import yaml


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_YAML = os.path.join(SCRIPT_DIR, "data", "config.yaml")

# 从配置文件读取 bitable 信息
bitable_cfg = yaml.safe_load(open(CONFIG_YAML))['bitable']
BITABLE_APP_TOKEN = bitable_cfg['app_token']
BITABLE_TABLE_ID = bitable_cfg['table_id']
BITABLE_API = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{BITABLE_APP_TOKEN}/tables/{BITABLE_TABLE_ID}/records"


# 11种方言列表（用于校验）
DIALECTS = ['哈尔滨话', '河南话', '湖南话', '天津话', '北京话', '上海话', '广东话', '东营方言', '重庆方言', '闽南话', '大连话']


def get_feishu_config():
    """获取飞书配置"""
    return yaml.safe_load(open(CONFIG_YAML))['feishu']


def get_bot_name():
    """通过飞书 /bot/v3/info API 获取当前应用的名字
    首次获取后自动写入 config.yaml，后续直接读取不再调用 API
    """
    all_cfg = yaml.safe_load(open(CONFIG_YAML))
    # 已有配置且非占位符，直接返回
    bot_name_cfg = all_cfg.get('bot_name', '')
    if bot_name_cfg and not bot_name_cfg.startswith('<'):
        return bot_name_cfg

    feishu_cfg = get_feishu_config()
    app_id = feishu_cfg['app_id']
    app_secret = feishu_cfg['app_secret']

    # 获取 token
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        data=data, headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as r:
        token = json.loads(r.read())['tenant_access_token']

    # 获取 bot 信息
    req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/bot/v3/info',
        headers={'Authorization': f'Bearer {token}'}
    )
    with urllib.request.urlopen(req) as r:
        bot_info = json.loads(r.read())

    bot_name = bot_info['bot']['app_name']

    # 首次获取，自动写入配置文件（只写一次，后续不再调用 API）
    all_cfg['bot_name'] = bot_name
    with open(CONFIG_YAML, 'w') as f:
        yaml.safe_dump(all_cfg, f, allow_unicode=True, default_flow_style=False)

    return bot_name


def get_token():
    """获取飞书 tenant_access_token"""
    feishu_cfg = get_feishu_config()

    # 读取云端共享开关
    cloud_cfg = yaml.safe_load(open(CONFIG_YAML)).get('cloud_share', {})
    if not cloud_cfg.get('enabled', False):
        print("⚠️ 云端共享未开启（cloud_share.enabled: false），跳过写入云表")
        print("如需开启，请修改 data/config.yaml：cloud_share.enabled: true")
        return None
    data = json.dumps({"app_id": feishu_cfg['app_id'], "app_secret": feishu_cfg['app_secret']}).encode()
    req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        data=data, headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())
    if resp.get('code') != 0:
        raise Exception(f"获取token失败: {resp}")
    return resp['tenant_access_token']


def add_record(token, std_word, dial_word, dial_name, category, remark, contributor):
    """
    写入一条记录到 bitable

    写入字段：
    - 普通话：标准语词汇
    - 方言词：方言表达（原来叫哈尔滨话字段，现已改名为方言词）
    - 词性：词汇分类
    - 补充人：贡献者名称
    - 添加日期：当前日期
    - 备注：补充说明
    - 方言：方言区（新增字段，支持11种方言）
    """
    # 添加日期（毫秒时间戳，当天零点）
    from datetime import datetime
    add_date_ms = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)

    payload = {
        "fields": {
            "普通话": std_word,
            "方言词": dial_word,
            "词性": category,
            "补充人": contributor,
            "添加日期": add_date_ms,
            "备注": remark,
            "方言": dial_name,  # 新增字段：写入方言区
        }
    }

    req = urllib.request.Request(
        BITABLE_API,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())

    if result.get('code') == 0:
        print(f"✅ 云端写入成功: {std_word} → {dial_word}（{dial_name}）")
        return True
    else:
        print(f"❌ 云端写入失败: {result.get('msg')} (code={result.get('code')})")
        return False


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    std_word = sys.argv[1]
    dial_word = sys.argv[2]
    dial_name = sys.argv[3] if len(sys.argv) > 3 else "哈尔滨话"
    category = sys.argv[4] if len(sys.argv) > 4 else "动词"
    remark = sys.argv[5] if len(sys.argv) > 5 else ""

    # 校验方言区是否合法
    if dial_name not in DIALECTS:
        print(f"⚠️ 方言区「{dial_name}」不在支持列表中，已自动设为哈尔滨话")
        dial_name = "哈尔滨话"

    try:
        contributor = get_bot_name()
    except Exception:
        contributor = '未知应用'

    try:
        token = get_token()
        if token is None:
            print(f"⚠️ 云端共享未开启，补充人：{contributor}")
            sys.exit(0)
        success = add_record(token, std_word, dial_word, dial_name, category, remark, contributor)
        if success:
            print(f"🎉 同步完成！补充人：{contributor}")
        else:
            print("⚠️ 云端写入失败，可能是没有权限（请联系管理员在飞书里给虾加权限）")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()