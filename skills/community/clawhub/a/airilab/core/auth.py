#!/usr/bin/env python3
"""
Unified auth manager for AiriLab.
"""

from datetime import datetime
from typing import Any, Dict

import requests

try:
    from .config import AiriLabConfig
except ImportError:  # pragma: no cover
    from config import AiriLabConfig

SEND_OTP_URL = 'https://cn.airilab.com/api/Accounts/Login'
VERIFY_CODE_URL = 'https://cn.airilab.com/api/Accounts/Login'
USER_INFO_URL = 'https://cn.airilab.com/api/user/getUserInfo'

DEFAULT_HEADERS = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,fr;q=0.8',
    'content-type': 'application/json',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}


class AiriLabAuth:
    """AiriLab unified authentication manager."""

    def __init__(self, config: AiriLabConfig = None):
        self.config = config or AiriLabConfig()

    def ensure_authenticated(self) -> Dict[str, Any]:
        token = self.config.get_token()

        if not token:
            return {
                'authenticated': False,
                'needs_login': True,
                'token': None,
                'message': 'Token not found, login required',
            }

        if not self.config.is_token_valid(token):
            return {
                'authenticated': False,
                'needs_login': True,
                'token': None,
                'message': 'Token format invalid or expired',
            }

        if not self.validate_token(token):
            return {
                'authenticated': False,
                'needs_login': True,
                'token': None,
                'message': 'Token expired, login required',
            }

        return {
            'authenticated': True,
            'needs_login': False,
            'token': token,
            'message': 'authenticated',
        }

    def validate_token(self, token: str) -> bool:
        headers = DEFAULT_HEADERS.copy()
        headers['Authorization'] = f'Bearer {token}'

        try:
            response = requests.get(USER_INFO_URL, headers=headers, timeout=10)
            return response.status_code == 200
        except Exception:
            return False

    def send_verification_code(self, phone: str, country_code: str = '+86') -> Dict[str, Any]:
        payload = {
            'phoneNumber': phone,
            'email': '',
            'isAgreedToTerms': True,
            'role': 2,
            'code': '',
            'countryCode': country_code,
            'countryName': 'China',
            'openId': '',
            'language': 'chs',
        }

        headers = DEFAULT_HEADERS.copy()
        headers['origin'] = 'http://localhost:3000'
        headers['referer'] = 'http://localhost:3000/'

        try:
            response = requests.post(SEND_OTP_URL, headers=headers, json=payload, timeout=30)
            result = response.json()

            status = result.get('status')
            message = str(result.get('message', '')).strip()

            # Strict success rule: only this tuple means OTP has been sent.
            if status == 200 and message == 'Otp sent':
                user_id = result.get('data')
                temp_state = {
                    'pendingPhone': phone,
                    'pendingUserId': user_id,
                    'pendingCountryCode': country_code,
                }
                return {
                    'success': True,
                    'message': message,
                    'user_id': user_id,
                    'temp_state': temp_state,
                    'raw': result,
                }

            # Any non-matching response is failure, forward backend message directly.
            return {
                'success': False,
                'message': message or 'Unknown error',
                'user_id': None,
                'raw': result,
            }

        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'user_id': None,
            }
        except ValueError:
            return {
                'success': False,
                'message': 'Invalid JSON response from server',
                'user_id': None,
            }

    def verify_code(self, phone: str, code: str, country_code: str = '+86') -> Dict[str, Any]:
        payload = {
            'phoneNumber': phone,
            'email': '',
            'isAgreedToTerms': True,
            'role': 2,
            'code': code,
            'countryCode': country_code,
            'countryName': 'China',
            'openId': '',
            'language': 'chs',
        }

        headers = DEFAULT_HEADERS.copy()
        headers['origin'] = 'https://cn.airilab.com'
        headers['referer'] = 'https://cn.airilab.com/stdio/sign-in'

        try:
            response = requests.post(VERIFY_CODE_URL, headers=headers, json=payload, timeout=30)
            result = response.json()

            if result.get('status') == 200 and result.get('message') == 'Success':
                data = result.get('data', {})
                access_token = data.get('accessToken')
                expires_in = int(data.get('expiresIn', 604800000))
                expires_at = int(datetime.now().timestamp() * 1000) + expires_in
                self.config.save_token(access_token, phone)

                return {
                    'success': True,
                    'token': access_token,
                    'message': 'Login successful',
                    'expires_at': expires_at,
                    'expires_days': expires_in // (1000 * 60 * 60 * 24),
                }

            return {
                'success': False,
                'message': result.get('message', 'Verification failed'),
                'token': None,
            }

        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'token': None,
            }
        except ValueError:
            return {
                'success': False,
                'message': 'Invalid JSON response from server',
                'token': None,
            }

    def logout(self) -> bool:
        return self.config.clear_token()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='AiriLab auth manager')
    parser.add_argument('action', choices=['status', 'login', 'logout', 'validate'], help='action')
    parser.add_argument('--phone', help='Phone number')
    parser.add_argument('--code', help='Verification code')

    args = parser.parse_args()

    auth = AiriLabAuth()

    if args.action == 'status':
        result = auth.ensure_authenticated()
        print(f"auth_status: {result['message']}")
        if result['authenticated']:
            token_preview = f"{result['token'][:20]}..." if result['token'] else None
            print(f'token: {token_preview}')

    elif args.action == 'login':
        if not args.phone:
            print('error: login requires --phone')
        elif not args.code:
            result = auth.send_verification_code(args.phone)
            print(result['message'])
        else:
            result = auth.verify_code(args.phone, args.code)
            if result['success']:
                print(result['message'])
                print(f"expires_days: {result['expires_days']}")
            else:
                print(result['message'])

    elif args.action == 'logout':
        auth.logout()
        print('logged out')

    elif args.action == 'validate':
        token = auth.config.get_token()
        if token:
            print('token_valid' if auth.validate_token(token) else 'token_invalid')
        else:
            print('token_missing')
