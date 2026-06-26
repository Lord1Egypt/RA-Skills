#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discover seamless automatic captcha solving with capsolver AI-powered Auto Web Unblock technology!
Supports automatic resolution of Geetest, reCAPTCHA v2, reCAPTCHA v3, MTCaptcha, DataDome, AWS WAF, Cloudflare Turnstile, and Cloudflare Challenge, etc.
"""

import os
import sys
import json
import time
import argparse
from typing import Optional, Dict, Any

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class CapSolver:
    SUPPORTED_TYPES = [
        # Task(Recognition)
        'ImageToTextTask',
        'ReCaptchaV2Classification',
        'AwsWafClassification',
        'VisionEngine',

        # Task(Token)
        'GeeTestTaskProxyLess',
        'ReCaptchaV2TaskProxyLess',
        'ReCaptchaV2EnterpriseTask',
        'ReCaptchaV2EnterpriseTaskProxyLess',
        'ReCaptchaV3Task',
        'ReCaptchaV3TaskProxyLess',
        'ReCaptchaV3EnterpriseTask',
        'ReCaptchaV3EnterpriseTaskProxyLess',
        'MtCaptchaTask',
        'MtCaptchaTaskProxyLess',
        'DatadomeSliderTask',
        'AntiAwsWafTask',
        'AntiAwsWafTaskProxyLess',
        'AntiTurnstileTaskProxyLess',
        'AntiCloudflareTask',
    ]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError(
                'API key not found. Please set API_KEY in .env file or environment variable.'
            )

        self.api_base = 'https://api.capsolver.com'
        self.create_task_endpoint = '/createTask'
        self.get_task_result_endpoint = '/getTaskResult'
        self.get_balance_endpoint = '/getBalance'
        self.timeout = 60
        self.interval = 1
        self.create_task_payload = {
            'source': 'capsolver-skill',
            'clientKey': self.api_key,
            'task': {}
        }
        self.get_task_result_payload = {
            'source': 'capsolver-skill',
            'clientKey': self.api_key,
            'taskId': ''
        }
        self.headers = {
            'Content-Type': 'application/json',
        }

    def check_type(self, _type: str) -> bool:
        return _type in self.SUPPORTED_TYPES

    def solve(self, args: argparse.Namespace) -> Dict[str, Any]:
        if not self.check_type(args.command):
            raise ValueError(f"Unsupported type: {args.command}. Supported: {', '.join(self.SUPPORTED_TYPES)}")

        self.build_task_payload(args)
        task_id, solution = self.create_task()
        if solution is not None:
            return solution
        return self.get_result(
            task_id=task_id,
            max_retries=args.max_retries
        )

    def build_task_payload(self, args: argparse.Namespace):
        if args.command == 'ImageToTextTask':
            if args.module == 'common' and args.body is None:
                raise ValueError('Body cannot be empty')
            if args.module == 'number' and args.images is None:
                raise ValueError('Images cannot be empty')
            self.create_task_payload['task'] = {
                'type': args.command,
                'websiteURL': args.websiteURL,
                'body': args.body,
                'images': args.images,
                'module': args.module
            }
        elif args.command == 'ReCaptchaV2Classification':
            self.create_task_payload['task'] = {
                'type': args.command,
                'websiteURL': args.websiteURL,
                'image': args.image,
                'question': args.question
            }
        elif args.command == 'AwsWafClassification':
            self.create_task_payload['task'] = {
                'type': args.command,
                'websiteURL': args.websiteURL,
                'images': args.images,
                'question': args.question
            }
        elif args.command == 'VisionEngine':
            self.create_task_payload['task'] = {
                'type': args.command,
                'websiteURL': args.websiteURL,
                'module': args.module,
                'image': args.image,
                'imageBackground': args.imageBackground,
                'question': args.question
            }
        elif args.command == 'GeeTestTaskProxyLess':
            self.create_task_payload['task'] = {
                'type': args.command,
                'websiteURL': args.websiteURL,
                'gt': args.gt,
                'challenge': args.challenge,
                'captchaId': args.captchaId,
                'geetestApiServerSubdomain': args.geetestApiServerSubdomain
            }
        elif 'ReCaptchaV2' in args.command:
            if args.command == 'ReCaptchaV2EnterpriseTask' and args.proxy is None:
                raise ValueError('Proxy cannot be empty')
            self.create_task_payload['task'] = {
                'type': args.command,
                'websiteURL': args.websiteURL,
                'websiteKey': args.websiteKey,
                'proxy': args.proxy,
                'pageAction': args.pageAction,
                'enterprisePayload': args.enterprisePayload,
                'isInvisible': args.isInvisible,
                'isSession': args.isSession
            }
        elif 'ReCaptchaV3' in args.command:
            if (args.command == 'ReCaptchaV3Task' or args.command == 'ReCaptchaV3EnterpriseTask') and args.proxy is None:
                raise ValueError('Proxy cannot be empty')
            self.create_task_payload['task'] = {
                'type': args.command,
                'websiteURL': args.websiteURL,
                'websiteKey': args.websiteKey,
                'proxy': args.proxy,
                'pageAction': args.pageAction,
                'enterprisePayload': args.enterprisePayload,
                'isSession': args.isSession
            }
        elif 'MtCaptchaTask' in args.command:
            if args.command == 'MtCaptchaTask' and args.proxy is None:
                raise ValueError('Proxy cannot be empty')
            self.create_task_payload['task'] = {
                'type': args.command,
                'websiteURL': args.websiteURL,
                'websiteKey': args.websiteKey,
                'proxy': args.proxy
            }
        elif args.command == 'DatadomeSliderTask':
            self.create_task_payload['task'] = {
                'type': args.command,
                'captchaUrl': args.captchaUrl,
                'userAgent': args.userAgent,
                'proxy': args.proxy
            }
        elif 'AntiAwsWafTask' in args.command:
            if args.command == 'AntiAwsWafTask' and args.proxy is None:
                raise ValueError('Proxy cannot be empty')
            self.create_task_payload['task'] = {
                'type': args.command,
                'websiteURL': args.websiteURL,
                'proxy': args.proxy,
                'awsKey': args.awsKey,
                'awsIv': args.awsIv,
                'awsContext': args.awsContext,
                'awsChallengeJS': args.awsChallengeJS,
                'awsApiJs': args.awsApiJs,
                'awsProblemUrl': args.awsProblemUrl,
                'awsApiKey': args.awsApiKey,
                'awsExistingToken': args.awsExistingToken
            }
        elif args.command == 'AntiTurnstileTaskProxyLess':
            self.create_task_payload['task'] = {
                'type': args.command,
                'websiteURL': args.websiteURL,
                'websiteKey': args.websiteKey,
                'metadata': {
                    'action': args.action,
                    'cdata': args.cdata,
                }
            }
        elif args.command == 'AntiCloudflareTask':
            if args.proxy is None:
                raise ValueError('Proxy cannot be empty')
            self.create_task_payload['task'] = {
                'type': args.command,
                'websiteURL': args.websiteURL,
                'userAgent': args.userAgent,
                'html': args.html,
                'proxy': args.proxy
            }
        else:
            raise TypeError(f"Unsupported type: {args.command}")

    def create_task(self) -> tuple[str, Any]:
        response = requests.post(
            f"{self.api_base}{self.create_task_endpoint}",
            headers=self.headers,
            json=self.create_task_payload,
            timeout=self.timeout
        )
        if response.status_code == 200:
            result = response.json()
            task_id = result.get("taskId")
            status = result.get('status')
            if not task_id:
                raise RuntimeError(f"Failed to create task, get taskId failed: {response.text}")
            if status == 'ready':
                return task_id, result.get('solution')
            return task_id, None
        if response.status_code == 400:
            result = response.json()
            error_description = result.get("errorDescription")
            raise ValueError(f"Failed to create task, invalid task: {error_description}")
        if response.status_code == 401:
            result = response.json()
            error_description = result.get("errorDescription")
            raise RuntimeError(f"Failed to create task, authentication failed: {error_description}")
        else:
            raise RuntimeError(f"Failed to create task, unexpected error {response.status_code}: {response.text}")

    def get_result(self, task_id: str, max_retries: int = 30) -> Dict[str, Any]:
        for attempt in range(1, max_retries + 1):
            result = self.get_task_result(task_id)

            if result is not None:
                return result

            if attempt < max_retries:
                print(f"Task {task_id} still pending, waiting {self.interval} seconds")
                time.sleep(self.interval)
        raise TimeoutError(f"Get task result failed after {max_retries} attempts.")

    def get_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        self.get_task_result_payload['taskId'] = task_id
        response = requests.post(
            f"{self.api_base}{self.get_task_result_endpoint}",
            headers=self.headers,
            json=self.get_task_result_payload,
            timeout=self.timeout
        )

        if response.status_code == 200:
            result = response.json()
            status = result.get('status')

            if status == 'ready':
                return result.get('solution')
            elif status in ['idle', 'processing']:
                return None
            elif status == 'failed':
                raise RuntimeError(f"Get task result failed: {result}")
        elif response.status_code == 400:
            result = response.json()
            error_description = result.get("errorDescription")
            raise ValueError(f"Failed to get task result, invalid task: {error_description}")
        else:
            raise RuntimeError(f"Unexpected status code {response.status_code}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Discover seamless automatic captcha solving with capsolver AI-powered Auto Web Unblock technology!',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
    API_KEY: Your CapSolver API key (required)

Examples:
    # ImageToTextTask
    python3 solver.py ImageToTextTask --body "base64_image_data"
    python3 solver.py ImageToTextTask --body "base64_image_data" --module "module_001"
    
    # ReCaptchaV2Classification
    python3 solver.py ReCaptchaV2Classification --question "question" --image "base64_image_data"
    
    # AwsWafClassification
    python3 solver.py AwsWafClassification --question "question" --images "base64_image_data1" "base64_image_data2" "base64_image_data3"
    
    # VisionEngine
    python3 solver.py VisionEngine --module "module" --image "base64_image_data" --imageBackground "base64_image_background_data"
    
    # GeeTest
    python3 solver.py GeeTestTaskProxyLess --websiteURL "https://example.com/" --captchaId "captcha_id"
    
    # reCAPTCHA v2
    python3 solver.py ReCaptchaV2TaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
    python3 solver.py ReCaptchaV2Task --websiteURL "https://example.com" --websiteKey "site_key" --proxy "host:port:username:password"

    # reCAPTCHA v3
    python3 solver.py ReCaptchaV3TaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
    python3 solver.py ReCaptchaV3Task --websiteURL "https://example.com" --websiteKey "site_key" --proxy "host:port:username:password"
    
    # MTCaptcha
    python3 solver.py MtCaptchaTaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
    python3 solver.py MtCaptchaTask --websiteURL "https://example.com" --websiteKey "site_key" --proxy "host:port:username:password"
    
    # DataDome
    python3 solver.py DatadomeSliderTask --captchaUrl "https://geo.captcha-delivery.com/xxxxxxxxx" --userAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36" --proxy "host:port:username:password"

    # AwsWaf
    python3 solver.py AntiAwsWafTask --websiteURL "https://example.com" --awsChallengeJS "https://path/to/challenge.js" --proxy "host:port:username:password"
    python3 solver.py AntiAwsWafTaskProxyLess --websiteURL "https://example.com" --awsChallengeJS "https://path/to/challenge.js"
    python3 solver.py AntiAwsWafTaskProxyLess --websiteURL "https://example.com"

    # Cloudflare Turnstile
    python3 solver.py AntiTurnstileTaskProxyLess --websiteURL "https://example.com" --websiteKey "site_key"
    
    # Cloudflare Challenge
    python3 solver.py AntiCloudflareTask --websiteURL "https://example.com" --proxy "host:port:username:password"
 
For detailed documentation, visit: https://docs.capsolver.com/
    """)

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # ========== Task(Recognition)
    # ImageToTextTask
    parser_image_to_text_task = subparsers.add_parser('ImageToTextTask', help='Solve text-based captcha')
    parser_image_to_text_task.add_argument('-u', '--websiteURL', required=False, help='Page source url to improve accuracy')
    parser_image_to_text_task.add_argument('-b', '--body', required=False, help='Base64 encoded content of the image (no newlines, no data:image/***;charset=utf-8;base64,)')
    parser_image_to_text_task.add_argument('-i', '--images', nargs='+', required=False, help='Only for number module, Support up to 9 base64 encoded images each time')
    parser_image_to_text_task.add_argument('-m', '--module', default='common', required=False, help='Specify the module. All supported module references: https://docs.capsolver.com/en/guide/recognition/ImageToTextTask/#independent-module-support')
    parser_image_to_text_task.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')
    # ReCaptchaV2Classification
    parser_recaptcha_v2_classification = subparsers.add_parser('ReCaptchaV2Classification', help='Classify reCAPTCHA v2 images')
    parser_recaptcha_v2_classification.add_argument('-u', '--websiteURL', required=False, help='Page source url to improve accuracy')
    parser_recaptcha_v2_classification.add_argument('-k', '--websiteKey', required=False, help='Website key to improve accuracy')
    parser_recaptcha_v2_classification.add_argument('-q', '--question', required=True, help='Please refer to: https://docs.capsolver.com/guide/recognition/ReCaptchaClassification/')
    parser_recaptcha_v2_classification.add_argument('-i', '--image', required=True, help='Base64 image string')
    parser_recaptcha_v2_classification.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')
    # AwsWafClassification
    parser_aws_waf_classification = subparsers.add_parser('AwsWafClassification', help='Classify aws waf images')
    parser_aws_waf_classification.add_argument('-u', '--websiteURL', required=False, help='Page source url to improve accuracy')
    parser_aws_waf_classification.add_argument('-q', '--question', required=True, help='Please refer to: https://docs.capsolver.com/guide/recognition/AwsWafClassification/')
    parser_aws_waf_classification.add_argument('-i', '--images', nargs='+', required=True, help='Base64 image string, aws:grid supports 9 images each time, other types support 1 image each time')
    parser_aws_waf_classification.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')
    # VisionEngine
    parser_vision_engine = subparsers.add_parser('VisionEngine', help='Advanced AI vision-based captcha solving')
    parser_vision_engine.add_argument('-u', '--websiteURL', required=False, help='Page source url to improve accuracy')
    parser_vision_engine.add_argument('-m', '--module', required=True, help='Please refer to: https://docs.capsolver.com/guide/recognition/VisionEngine/')
    parser_vision_engine.add_argument('-q', '--question', required=False, help='Only the shein model requires, please refer to: https://docs.capsolver.com/en/guide/recognition/VisionEngine/')
    parser_vision_engine.add_argument('-i', '--image', required=True, help='Base64 encoded content of the image (no newlines, no data:image/***;charset=utf-8;base64,)')
    parser_vision_engine.add_argument('-b', '--imageBackground', required=False, help='Base64 encoded content of the background image (no newlines, no data:image/***;charset=utf-8;base64,)')
    parser_vision_engine.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')

    # ========== Task(Token)
    # GeeTestTaskProxyLess
    parser_geetest_task_proxyless = subparsers.add_parser('GeeTestTaskProxyLess', help='Solve GeeTest captcha (v3/v4)')
    parser_geetest_task_proxyless.add_argument('-u', '--websiteURL', required=True, help='Web address of the website using geetest (Ex: https://geetest.com)')
    parser_geetest_task_proxyless.add_argument('-g', '--gt', required=False, help='Only Geetest V3 is required')
    parser_geetest_task_proxyless.add_argument('-c', '--challenge', required=False, help='Only Geetest V3 is required')
    parser_geetest_task_proxyless.add_argument('-i', '--captchaId', required=False, help='Only Geetest V4 is required')
    parser_geetest_task_proxyless.add_argument('-d', '--geetestApiServerSubdomain', required=False, help='Special api subdomain, example: api.geetest.com')
    parser_geetest_task_proxyless.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')
    # ReCaptchaV2TaskProxyLess
    # ReCaptchaV2EnterpriseTask
    # ReCaptchaV2EnterpriseTaskProxyLess
    parser_recaptcha_v2_name_list = ['ReCaptchaV2TaskProxyLess', 'ReCaptchaV2EnterpriseTask', 'ReCaptchaV2EnterpriseTaskProxyLess']
    for parser_recaptcha_v2_name in parser_recaptcha_v2_name_list:
        parser_recaptcha_v2 = subparsers.add_parser(parser_recaptcha_v2_name, help='Solve Google reCAPTCHA v2 (checkbox/invisible)')
        parser_recaptcha_v2.add_argument('-u', '--websiteURL', required=True, help='The URL of the target webpage that loads the captcha, It’s best to submit the full URL instead of just the host')
        parser_recaptcha_v2.add_argument('-k', '--websiteKey', required=True, help='Recaptcha website key')
        parser_recaptcha_v2.add_argument('-p', '--proxy', required=False, help='Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/')
        parser_recaptcha_v2.add_argument('-a', '--pageAction', required=False, help='For ReCaptcha v2, if there is an sa parameter in the payload of the /anchor endpoint, please submit its value')
        parser_recaptcha_v2.add_argument('-e', '--enterprisePayload', required=False, help='For ReCaptchaV2 enterprise version, if there is an s parameter in the payload of the /anchor endpoint, please submit its value')
        parser_recaptcha_v2.add_argument('-i', '--isInvisible', type=bool, default=False, required=False, help='Pass true if there is no “I’m not a robot” checkbox but the challenge will still appear, usually required in v2 invisible mode')
        parser_recaptcha_v2.add_argument('-s', '--isSession', type=bool, default=False, required=False, help='Session mode, when enabled, will return a recaptcha-ca-t value, which is used as a cookie. It usually appears in v3. Note: Some websites require a recaptcha-ca-e value, which usually appears in v2. If this value is present, it will be automatically returned without any additional parameter settings')
        parser_recaptcha_v2.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')
    # ReCaptchaV3Task
    # ReCaptchaV3TaskProxyLess
    # ReCaptchaV3EnterpriseTask
    # ReCaptchaV3EnterpriseTaskProxyLess
    parser_recaptcha_v3_name_list = ['ReCaptchaV3Task', 'ReCaptchaV3TaskProxyLess', 'ReCaptchaV3EnterpriseTask', 'ReCaptchaV3EnterpriseTaskProxyLess']
    for parser_recaptcha_v3_name in parser_recaptcha_v3_name_list:
        parser_recaptcha_v3 = subparsers.add_parser(parser_recaptcha_v3_name, help='Solve Google reCAPTCHA v3')
        parser_recaptcha_v3.add_argument('-u', '--websiteURL', required=True, help='The URL of the target webpage that loads the captcha, It’s best to submit the full URL instead of just the host.')
        parser_recaptcha_v3.add_argument('-k', '--websiteKey', required=True, help='Recaptcha website key.')
        parser_recaptcha_v3.add_argument('-p', '--proxy', required=False, help='Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/')
        parser_recaptcha_v3.add_argument('-a', '--pageAction', required=False, help='For ReCaptcha v3, You can find the value of the action parameter by searching for grecaptcha.execute')
        parser_recaptcha_v3.add_argument('-e', '--enterprisePayload', required=False, help='For the enterprise version, search for grecaptcha.enterprise.render and pass the s parameter')
        parser_recaptcha_v3.add_argument('-s', '--isSession', type=bool, default=False, required=False, help='Session mode, when enabled, will return a recaptcha-ca-t value, which is used as a cookie. It usually appears in v3. Note: Some websites require a recaptcha-ca-e value, which usually appears in v2. If this value is present, it will be automatically returned without any additional parameter settings')
        parser_recaptcha_v3.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')
    # MtCaptchaTask
    # MtCaptchaTaskProxyLess
    parser_mtcaptcha_name_list = ['MtCaptchaTask', 'MtCaptchaTaskProxyLess']
    for parser_mtcaptcha_name in parser_mtcaptcha_name_list:
        parser_mtcaptcha = subparsers.add_parser(parser_mtcaptcha_name, help='Solve MTCaptcha')
        parser_mtcaptcha.add_argument('-u', '--websiteURL', required=True, help='Web address of the website using generally it’s fixed value. (Ex: https://google.com)')
        parser_mtcaptcha.add_argument('-k', '--websiteKey', required=True, help='The domain public key, rarely updated. (Ex: sk=MTPublic-xxx public key)')
        parser_mtcaptcha.add_argument('-p', '--proxy', required=False, help='Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/')
        parser_mtcaptcha.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')
    # DatadomeSliderTask
    parser_datadome_slider = subparsers.add_parser('DatadomeSliderTask', help='Solve DataDome')
    parser_datadome_slider.add_argument('-u', '--captchaUrl', required=True, help='If the url contains t=bv that means that your ip must be banned, t should be t=fe')
    parser_datadome_slider.add_argument('-a', '--userAgent', required=False, help='It needs to be the same as the userAgent you use to request the website. Currently we only support the following userAgent')
    parser_datadome_slider.add_argument('-p', '--proxy', required=False, help='Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/')
    parser_datadome_slider.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')
    # AntiAwsWafTask
    # AntiAwsWafTaskProxyLess
    parser_aws_waf_name_list = ['AntiAwsWafTask', 'AntiAwsWafTaskProxyLess']
    for parser_aws_waf_name in parser_aws_waf_name_list:
        parser_aws_waf = subparsers.add_parser(parser_aws_waf_name, help='Solve AWS WAF')
        parser_aws_waf.add_argument('-u', '--websiteURL', required=True, help='Web address of the website using generally it’s fixed value. (Ex: https://google.com)')
        parser_aws_waf.add_argument('-p', '--proxy', required=False, help='Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/')
        parser_aws_waf.add_argument('-k', '--awsKey', required=False, help='The key value returned by the captcha page')
        parser_aws_waf.add_argument('-i', '--awsIv', required=False, help='The iv value returned by the captcha page')
        parser_aws_waf.add_argument('-c', '--awsContext', required=False, help='The context value returned by the captcha page')
        parser_aws_waf.add_argument('-cj', '--awsChallengeJS', required=False, help='The challenge.js link returned by the captcha page')
        parser_aws_waf.add_argument('-aj', '--awsApiJs', required=False, help='The jsapi.js link returned by the captcha page')
        parser_aws_waf.add_argument('-pu', '--awsProblemUrl', required=False, help='The problem endpoint url containing keywords like problem, num_solutions_required, etc.')
        parser_aws_waf.add_argument('-ak', '--awsApiKey', required=False, help='The api_key value of the problem endpoint')
        parser_aws_waf.add_argument('-et', '--awsExistingToken', required=False, help='The aws-waf-token used for the last verification')
        parser_aws_waf.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')
    # AntiTurnstileTaskProxyLess
    parser_anti_turnstile_task_proxyless = subparsers.add_parser('AntiTurnstileTaskProxyLess', help='Solve Cloudflare Turnstile')
    parser_anti_turnstile_task_proxyless.add_argument('-u', '--websiteURL', required=True, help='The address of the target page')
    parser_anti_turnstile_task_proxyless.add_argument('-k', '--websiteKey', required=True, help='Turnstile website key')
    parser_anti_turnstile_task_proxyless.add_argument('-a', '--action', required=False, help='The value of the data-action attribute of the Turnstile element if it exists')
    parser_anti_turnstile_task_proxyless.add_argument('-c', '--cdata', required=False, help='The value of the data-cdata attribute of the Turnstile element if it exists')
    parser_anti_turnstile_task_proxyless.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')
    # AntiCloudflareTask
    parser_anti_cloudflare_task = subparsers.add_parser('AntiCloudflareTask', help='Solve Cloudflare Challenge (5-second shield)')
    parser_anti_cloudflare_task.add_argument('-u', '--websiteURL', required=True, help='The address of the target page')
    parser_anti_cloudflare_task.add_argument('-p', '--proxy', required=False, help='Learn Using proxies: https://docs.capsolver.com/guide/api-how-to-use-proxy/')
    parser_anti_cloudflare_task.add_argument('-a', '--userAgent', required=False, help='The user-agent you used to request the target website. Only Chrome’s userAgent is supported')
    parser_anti_cloudflare_task.add_argument('-t', '--html', required=False, help='The response of requesting the target website, it usually contains "Just a moment…" and status code is 403. we need this html for some websites, please be sure to use your sticky proxy to dynamically scrape the HTML every time')
    parser_anti_cloudflare_task.add_argument('-r', '--max-retries', type=int, default=60, help='Maximum number of retries')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        solver = CapSolver()
        solution = solver.solve(args)
        print(json.dumps(solution, indent=2))
    except Exception as e:
        print('Solve failed:', e)
        sys.exit(1)


if __name__ == "__main__":
    main()
