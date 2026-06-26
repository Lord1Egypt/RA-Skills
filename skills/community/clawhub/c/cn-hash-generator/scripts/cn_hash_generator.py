#!/usr/bin/env python3
"""
cn-hash-generator - Hash生成器
支持多种Hash算法、Base64、UUID、HMAC
"""
import argparse
import hashlib
import uuid
import base64
import sys
import os

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def sha1_hash(text):
    return hashlib.sha1(text.encode()).hexdigest()

def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def sha512_hash(text):
    return hashlib.sha512(text.encode()).hexdigest()

def blake2b_hash(text):
    return hashlib.blake2b(text.encode()).hexdigest()

def hmac_sign(text, key, algo='sha256'):
    import hmac
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512,
    }
    algo_key = algo.lower()
    if algo_key not in algorithms:
        print(f"Unsupported algorithm: {algo}")
        return None
    h = hmac.new(key.encode('utf-8'), text.encode('utf-8'), algorithms[algo_key])
    return h.hexdigest()

def generate_uuid():
    return str(uuid.uuid4())

def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    return base64.b64decode(text.encode()).decode()

def main():
    parser = argparse.ArgumentParser(description='Hash生成器')
    parser.add_argument('text', nargs='?', help='Text to hash')
    parser.add_argument('--algo', default='sha256', 
                       choices=['md5', 'sha1', 'sha256', 'sha512', 'blake2'],
                       help='Hash算法')
    parser.add_argument('--encode64', action='store_true', help='Base64编码')
    parser.add_argument('--decode', action='store_true', help='Base64解码')
    parser.add_argument('--uuid', action='store_true', help='生成UUID')
    parser.add_argument('--hmac', metavar='KEY', help='HMAC密钥')
    parser.add_argument('--upper', action='store_true', help='输出大写')
    parser.add_argument('--count', type=int, default=1, help='生成数量')
    
    args = parser.parse_args()
    
    # UUID模式
    if args.uuid:
        for i in range(args.count):
            uid = generate_uuid()
            print(uid.upper() if args.upper else uid)
        return
    
    # Base64模式
    if args.encode64:
        if not args.text:
            print("Please provide text to encode")
            return
        result = base64_encode(args.text)
        print(result.upper() if args.upper else result)
        return
    
    if args.decode:
        if not args.text:
            print("Please provide text to decode")
            return
        try:
            result = base64_decode(args.text)
            print(result)
        except Exception as e:
            print(f"Decode failed: {e}")
        return
    
    # Hash模式
    if not args.text:
        # 尝试从stdin读取
        if not sys.stdin.isatty():
            args.text = sys.stdin.read().strip()
        else:
            print("Usage:")
            print("  python3 cn_hash_generator.py '文本' --algo sha256")
            print("  python3 cn_hash_generator.py --uuid")
            print("  python3 cn_hash_generator.py '文本' --encode64")
            print("  echo 'SGVsbG8=' | python3 cn_hash_generator.py --decode")
            return
    
    # HMAC模式
    if args.hmac:
        result = hmac_sign(args.text, args.hmac, args.algo)
        if result:
            print(result.upper() if args.upper else result)
        return
    
    # 普通Hash
    if args.algo == 'md5':
        result = md5_hash(args.text)
    elif args.algo == 'sha1':
        result = sha1_hash(args.text)
    elif args.algo == 'sha256':
        result = sha256_hash(args.text)
    elif args.algo == 'sha512':
        result = sha512_hash(args.text)
    elif args.algo == 'blake2':
        result = blake2b_hash(args.text)
    else:
        result = sha256_hash(args.text)
    
    print(result.upper() if args.upper else result)

if __name__ == '__main__':
    main()