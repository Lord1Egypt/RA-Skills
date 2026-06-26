#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CC Live Room Creation Script
使用 THQS 签名认证创建直播间
"""

import sys
import hashlib
import time
import urllib.parse
import requests


API_URL = 'https://api.csslcloud.net/api/room/create'


def my_urlencode(q):
    """URL encode with quote_plus, sorted by key"""
    l = []
    for k in q:
        k_encoded = urllib.parse.quote_plus(str(k))
        v_encoded = urllib.parse.quote_plus(str(q[k]))
        l.append('%s=%s' % (k_encoded, v_encoded))
    l.sort()
    return '&'.join(l)


def create_room(userid, api_key, name, templatetype=1, mobileViewMode=None):
    """
    Create a CC live streaming room

    Args:
        userid: CC account ID
        api_key: API key for THQS signature
        name: Room name (max 40 characters)
        templatetype: 1=大屏模式, 2=问答、视频、聊天, 3=视频、聊天,
                      4=文档、视频、聊天, 5=视频、文档、问答、聊天, 6=视频、问答
        mobileViewMode: Mobile view mode. 2=竖屏观看, None=使用默认(横屏)
                        Only applicable for templatetype 1, 2, 3, 6

    Returns:
        dict: API response containing roomid if successful
    """
    params = {
        'userid': userid,
        'name': name,
        'desc': '通过API接口创建的直播间',
        'templatetype': templatetype,
        'authtype': 2,  # 免密码登录
        'publisherpass': '123456',  # 推流端密码
        'assistantpass': '123456',  # 助教端密码
    }

    if mobileViewMode is not None:
        params['mobileViewMode'] = mobileViewMode

    # Generate THQS signature
    qftime = 'time=%d' % int(time.time())
    salt = 'salt=%s' % api_key
    qftail = '&%s&%s' % (qftime, salt)

    qs = my_urlencode(params)
    qf = qs + qftail

    hashqf = 'hash=%s' % (hashlib.new('md5', qf.encode('utf-8')).hexdigest().upper())
    thqs = '&'.join((qs, qftime, hashqf))

    url = '%s?%s' % (API_URL, thqs)

    print('Requesting: %s' % url)

    try:
        resp = requests.get(url, timeout=30)
        print('Response: %s' % resp.text)
        return resp.json()
    except Exception as e:
        print('Error: %s' % str(e))
        return {'error': str(e)}


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python create_room.py <userid> <api_key> <room_name> [templatetype] [mobileViewMode]')
        print('  templatetype: 1-6 (default: 1)')
        print('  mobileViewMode: 2=竖屏观看, not set=横屏(default)')
        print('  Note: mobileViewMode only applies to templatetype 1, 2, 3, 6')
        sys.exit(1)

    userid = sys.argv[1]
    api_key = sys.argv[2]
    name = sys.argv[3]
    templatetype = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    mobileViewMode = int(sys.argv[5]) if len(sys.argv) > 5 else None

    result = create_room(userid, api_key, name, templatetype, mobileViewMode)

    if result.get('result') == 'OK' and 'room' in result:
        print('\n=== 直播间创建成功 ===')
    else:
        print('\n=== 创建失败 ===')
        print(result)
