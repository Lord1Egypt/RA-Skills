#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test BioLIMS API"""
import requests
import json
import time
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

BASE_URL = os.environ.get("BIOLIMS_URL", "http://example.com/biolims")
USERNAME = os.environ.get("BIOLIMS_USER", "demo")
PASSWORD = os.environ.get("BIOLIMS_PASSWORD", "demo")
DATA_SOURCE = os.environ.get("BIOLIMS_DS", "demo")

# Encryption parameters
AES_KEY = os.environ.get("BIOLIMS_AES_KEY", "0000000000000000").encode('utf-8')
AES_IV = os.environ.get("BIOLIMS_AES_IV", "0000000000000000").encode('utf-8')
SECRET_KEY = os.environ.get("BIOLIMS_SECRET", "demo")


def encrypt_password(password):
    """Encrypt password using AES-CBC"""
    data = {
        "password": password,
        "captCode": "",
        "time": int(time.time() * 1000),
        "secretKey": SECRET_KEY
    }
    plaintext = json.dumps(data)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    encrypted = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted).decode('utf-8')


def login(session):
    """Login to obtain Token"""
    encrypted_pwd = encrypt_password(PASSWORD)
    url = f"{BASE_URL}/user/Login"
    headers = {
        "Content-Type": "application/json",
        "code": DATA_SOURCE,
        "accept-language": "zh_CN"
    }
    params = {
        "username": USERNAME,
        "password": encrypted_pwd
    }

    print(f"Login URL: {url}")
    print(f"Encrypted password: {encrypted_pwd}")

    response = session.post(url, params=params, headers=headers)

    print(f"Status code: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Cookies: {dict(response.cookies)}")
    print(f"Response body: {response.text[:500]}")

    if response.status_code == 200:
        token = response.headers.get('token') or response.headers.get('Token')
        if token:
            print(f"\n✓ Token obtained successfully: {token}")
            return token
        else:
            print("\n✗ Token not found")
            return None
    else:
        print(f"\n✗ Login failed")
        return None


def query_orders(session, token):
    """Query order list"""
    url = f"{BASE_URL}/order/selectAllOrderList"

    # Get XSRF token
    xsrf_token = session.cookies.get('XSRF-TOKEN', '')

    headers = {
        "Content-Type": "application/json",
        "Token": token,
        "X-DS": DATA_SOURCE,
        "X-XSRF-TOKEN": xsrf_token,
        "accept-language": "zh_CN"
    }
    payload = {
        "bioTechLeaguePagingQuery": {
            "page": 1,
            "rows": 2,
            "sort": {},
            "query": []
        }
    }

    print(f"\nQuery orders URL: {url}")
    print(f"Request headers: {headers}")
    print(f"Session Cookies: {dict(session.cookies)}")
    print(f"Request body: {json.dumps(payload, indent=2)}")

    response = session.post(url, json=payload, headers=headers)

    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text[:1000]}")


if __name__ == "__main__":
    print("=== Test BioLIMS API ===\n")

    # Create session to maintain cookies
    session = requests.Session()

    # 1. Login
    print("1. Login to obtain Token")
    print("-" * 50)
    token = login(session)

    if token:
        # 2. Query orders
        print("\n2. Query order list")
        print("-" * 50)
        query_orders(session, token)
    else:
        print("\nLogin failed, cannot continue testing")
