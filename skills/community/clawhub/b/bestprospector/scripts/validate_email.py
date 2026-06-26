#!/usr/bin/env python3
"""
验证邮箱地址有效性
支持格式验证、域名DNS检查
"""

import argparse
import json
import re
import sys
import socket
import dns.resolver

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

DISPOSABLE_DOMAINS = [
    'tempmail.com', 'guerrillamail.com', 'mailinator.com', '10minutemail.com',
    'throwaway.email', 'fakeinbox.com', 'temp-mail.org', 'dispostable.com',
]


def validate_format(email):
    if not email or not isinstance(email, str):
        return False, "Empty or invalid type"
    
    email = email.strip().lower()
    
    if not EMAIL_PATTERN.match(email):
        return False, "Invalid email format"
    
    local, domain = email.split('@')
    
    if len(local) < 1 or len(local) > 64:
        return False, "Local part length invalid"
    
    if len(domain) < 4 or len(domain) > 255:
        return False, "Domain length invalid"
    
    if '..' in email:
        return False, "Consecutive dots not allowed"
    
    return True, "Valid format"


def check_domain_mx(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        if records:
            return True, f"MX records found: {len(records)}"
        return False, "No MX records found"
    except dns.resolver.NXDOMAIN:
        return False, "Domain does not exist"
    except dns.resolver.NoAnswer:
        try:
            records = dns.resolver.resolve(domain, 'A')
            if records:
                return True, "Domain exists (A record, no MX)"
            return False, "No DNS records found"
        except:
            return False, "No DNS records found"
    except Exception as e:
        return False, f"DNS lookup error: {str(e)}"


def is_disposable(domain):
    return domain.lower() in DISPOSABLE_DOMAINS


def validate_email(email, check_dns=True):
    result = {
        'email': email,
        'valid': False,
        'format_valid': False,
        'domain_valid': False,
        'disposable': False,
        'errors': []
    }
    
    format_valid, format_msg = validate_format(email)
    result['format_valid'] = format_valid
    
    if not format_valid:
        result['errors'].append(format_msg)
        return result
    
    local, domain = email.split('@')
    
    if is_disposable(domain):
        result['disposable'] = True
        result['errors'].append("Disposable email domain")
    
    if check_dns:
        try:
            domain_valid, domain_msg = check_domain_mx(domain)
            result['domain_valid'] = domain_valid
            if not domain_valid:
                result['errors'].append(domain_msg)
        except Exception as e:
            result['domain_valid'] = False
            result['errors'].append(f"DNS check failed: {str(e)}")
    else:
        result['domain_valid'] = True
    
    result['valid'] = result['format_valid'] and result['domain_valid'] and not result['disposable']
    
    return result


def validate_batch(emails, check_dns=True):
    results = []
    for email in emails:
        result = validate_email(email, check_dns)
        results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(description='Validate email addresses')
    parser.add_argument('email', nargs='?', help='Email address to validate')
    parser.add_argument('--batch', '-b', help='JSON file with email list')
    parser.add_argument('--no-dns', action='store_true', help='Skip DNS validation')
    parser.add_argument('--output', '-o', help='Output file path (JSON)')
    
    args = parser.parse_args()
    
    if args.batch:
        with open(args.batch, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            emails = data
        elif isinstance(data, dict) and 'emails' in data:
            emails = data['emails']
        else:
            print("Invalid batch file format", file=sys.stderr)
            sys.exit(1)
        
        results = validate_batch(emails, check_dns=not args.no_dns)
        
        output = {
            'total': len(results),
            'valid': sum(1 for r in results if r['valid']),
            'results': results
        }
        
    elif args.email:
        result = validate_email(args.email, check_dns=not args.no_dns)
        output = result
        
    else:
        parser.print_help()
        sys.exit(1)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"Results saved to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
