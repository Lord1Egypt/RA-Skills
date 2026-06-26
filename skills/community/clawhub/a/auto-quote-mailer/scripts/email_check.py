#!/usr/bin/env python3
"""
Single check for new emails and process them
单次检查新邮件并处理
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config'))

import config
from email_utils import (
    connect_to_imap,
    get_new_unread_messages,
    mark_as_read,
    ensure_storage_directories,
    generate_filename,
    save_raw_email,
    save_text_content,
    save_quote
)
from translator import translate_text
from quote_calculator import parse_customer_request, calculate_price, generate_quote_text, generate_quote_text_in_language

def process_single_email(msg, conn):
    """Process a single email"""
    print(f"Processing email: {msg['subject']} from {msg['from']}")
    
    # Generate filename
    filename_base = generate_filename()
    
    # Save raw email
    save_raw_email(filename_base, msg['raw_bytes'])
    print(f"  Raw email saved")
    
    # Save original text
    original_text = f"""Subject: {msg['subject']}
From: {msg['from']}
Date: {msg['date']}

--- Content ---
{msg['body']}
"""
    text_path = save_text_content(filename_base, original_text, is_translated=False)
    print(f"  Text saved: {text_path}")
    
    # Translate
    translated_text, was_translated = translate_text(msg['body'])
    if was_translated:
        translated_full = f"""Subject: {msg['subject']}
From: {msg['from']}
Date: {msg['date']}
Note: Original is not in target language, automatically translated

--- Translated Content ---
{translated_text}

--- Original ---
{msg['body']}
"""
        trans_path = save_text_content(filename_base, translated_full, is_translated=True)
        print(f"  Translation saved: {trans_path}")
        content_for_quote = translated_text
    else:
        content_for_quote = msg['body']
    
    # Try to parse requirements and generate quote
    try:
        request = parse_customer_request(content_for_quote)
        if request['material'] and request['size'] is not None:
            # Enough info to generate quote
            result = calculate_price(
                request['material'],
                request['size'],
                request['quantity'],
                request['processes']
            )
            # Generate quote in target language
            quote_target = generate_quote_text(result, config.COMPANY_INFO)
            quote_path_target = save_quote(filename_base + '_quote', quote_target)
            
            # If original was in different language, also generate quote in original language
            if was_translated:
                # Currently supports English output for foreign customers
                quote_original = generate_quote_text_in_language(result, config.COMPANY_INFO, lang='en')
                quote_path_original = save_quote(filename_base + '_quote_en', quote_original)
                print(f"  Bilingual quotes generated: target={quote_path_target}, original={quote_path_original}")
                quote_path = quote_path_target
            else:
                print(f"  Quote generated: {quote_path_target}")
                quote_path = quote_path_target
        else:
            # Insufficient information, save for manual processing
            quote = f"""Insufficient customer information to automatically generate quotation.

Extracted information:
- Material: {request['material'] or 'Not recognized'}
- Size: {request['size'] or 'Not recognized'}
- Quantity: {request['quantity']}
- Processes: {request['processes']}

Original content:
{content_for_quote}
"""
            if was_translated:
                quote += "\n--- Original ---\n" + msg['body']
            quote_path = save_quote(filename_base + '_manual', quote)
            print(f"  Insufficient information, saved for manual processing: {quote_path}")
            quote_path = None
    except Exception as e:
        print(f"  Error generating quote: {e}")
        import traceback
        traceback.print_exc()
        quote_path = None
    
    # Mark as read
    mark_as_read(conn, msg['uid'])
    
    return {
        'filename_base': filename_base,
        'was_translated': was_translated,
        'quote_generated': quote_path is not None,
    }

def main():
    print("Email Quote Automation - Single Check")
    print("=" * 40)
    
    # Ensure directories exist
    ensure_storage_directories()
    
    try:
        # Connect to email
        print("Connecting to email server...")
        conn = connect_to_imap()
        print("Connected successfully")
        
        # Get unread messages
        messages = get_new_unread_messages(conn)
        print(f"Found {len(messages)} unread messages")
        
        # Process each message
        processed = []
        for msg in messages:
            result = process_single_email(msg, conn)
            processed.append(result)
        
        print(f"\nProcessing complete! Processed {len(processed)} emails")
        for r in processed:
            status_quote = "✓" if r['quote_generated'] else "✗"
            status_trans = "T" if r['was_translated'] else "-"
            print(f"  - {r['filename_base']}: [{status_trans}] [{status_quote}]")
        
        conn.logout()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
