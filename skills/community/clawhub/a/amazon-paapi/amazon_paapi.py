#!/usr/bin/env python3
"""
Amazon Product Advertising API (PA API) Client
Einfacher Zugriff auf Amazon Produktinformationen
"""

import os
import sys
import json
import time
import hmac
import hashlib
import datetime
import requests
from urllib.parse import quote

class AmazonPAAPI:
    """Amazon Product Advertising API Client"""
    
    def __init__(self):
        self.access_key = os.getenv('AMAZON_ACCESS_KEY')
        self.secret_key = os.getenv('AMAZON_SECRET_KEY')
        self.partner_tag = os.getenv('AMAZON_PARTNER_TAG')
        self.marketplace = 'www.amazon.de'
        self.region = 'eu-west-1'
        self.service = 'ProductAdvertisingAPI'
        
        if not all([self.access_key, self.secret_key, self.partner_tag]):
            raise ValueError("❌ Credentials fehlen! Setze AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_PARTNER_TAG")
    
    def _sign(self, key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
    
    def _get_signature_key(self, secret_key, date_stamp, region_name, service_name):
        k_date = self._sign(('AWS4' + secret_key).encode('utf-8'), date_stamp)
        k_region = self._sign(k_date, region_name)
        k_service = self._sign(k_region, service_name)
        k_signing = self._sign(k_service, 'aws4_request')
        return k_signing
    
    def _make_request(self, payload):
        """Signierte API Request erstellen"""
        t = datetime.datetime.utcnow()
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')
        
        host = 'webservices.amazon.de'
        uri = '/paapi5/getitems'
        
        # Headers
        headers = {
            'Host': host,
            'Content-Type': 'application/json; charset=utf-8',
            'X-Amz-Date': amz_date,
            'X-Amz-Target': 'com.amazon.paapi5.v1.ProductAdvertisingAPIv1.GetItems'
        }
        
        # Request body
        body = json.dumps(payload)
        
        # Signature (vereinfacht - in Produktion besser mit aws4auth Library)
        # Für Demo: Direkter Request ohne komplexe Signatur
        
        response = requests.post(
            f'https://{host}{uri}',
            headers=headers,
            data=body,
            timeout=30
        )
        
        return response
    
    def get_item(self, asin):
        """Produktinformationen per ASIN abrufen"""
        payload = {
            'ItemIds': [asin],
            'Resources': [
                'Images.Primary.Large',
                'ItemInfo.Title',
                'Offers.Listings.Price',
                'CustomerReviews.StarRating'
            ],
            'PartnerTag': self.partner_tag,
            'PartnerType': 'Associates',
            'Marketplace': self.marketplace
        }
        
        try:
            # Rate limiting (1 Request/Sec max)
            time.sleep(1.1)
            
            response = self._make_request(payload)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_item(data, asin)
            else:
                return {'error': f'HTTP {response.status_code}', 'message': response.text}
                
        except Exception as e:
            return {'error': str(e)}
    
    def _parse_item(self, data, asin):
        """API Response parsen"""
        items_result = data.get('ItemsResult', {})
        items = items_result.get('Items', [])
        
        if not items:
            return {'error': 'Produkt nicht gefunden', 'asin': asin}
        
        item = items[0]
        
        result = {
            'asin': asin,
            'title': item.get('ItemInfo', {}).get('Title', {}).get('DisplayValue', 'N/A'),
            'url': item.get('DetailPageURL', ''),
            'image': item.get('Images', {}).get('Primary', {}).get('Large', {}).get('URL', ''),
        }
        
        # Preis extrahieren
        offers = item.get('Offers', {}).get('Listings', [])
        if offers:
            price_info = offers[0].get('Price', {})
            result['price'] = price_info.get('DisplayAmount', 'N/A')
            result['currency'] = price_info.get('Currency', 'EUR')
            result['amount'] = price_info.get('Amount', 0)
        else:
            result['price'] = 'N/A'
        
        # Bewertung
        reviews = item.get('CustomerReviews', {})
        if reviews:
            result['rating'] = reviews.get('StarRating', {}).get('DisplayValue', 'N/A')
        
        return result


def main():
    if len(sys.argv) < 2:
        print("Usage: ama-paapi <ASIN>")
        print("Example: ama-paapi B0BQXKDZGK")
        sys.exit(1)
    
    asin = sys.argv[1]
    
    try:
        client = AmazonPAAPI()
        result = client.get_item(asin)
        
        if 'error' in result:
            print(f"❌ Fehler: {result['error']}")
            if 'message' in result:
                print(f"Details: {result['message']}")
        else:
            print("✅ Produkt gefunden!")
            print(f"Titel: {result['title']}")
            print(f"Preis: {result['price']}")
            if 'rating' in result:
                print(f"Bewertung: {result['rating']}")
            print(f"URL: {result['url']}")
            
    except ValueError as e:
        print(e)
        print("\n🔧 Setup:")
        print("1. Amazon Associates Konto erstellen:")
        print("   https://affiliate-program.amazon.de/")
        print("2. PA API Credentials generieren")
        print("3. In ~/.env speichern:")
        print("   AMAZON_ACCESS_KEY=dein_key")
        print("   AMAZON_SECRET_KEY=dein_secret")
        print("   AMAZON_PARTNER_TAG=dein-tag-21")


if __name__ == '__main__':
    main()
