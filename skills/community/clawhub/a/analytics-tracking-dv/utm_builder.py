import argparse
import urllib.parse

def build_utm_url(url, source, medium, campaign, term=None, content=None):
    params = {
        'utm_source': source,
        'utm_medium': medium,
        'utm_campaign': campaign
    }
    if term:
        params['utm_term'] = term
    if content:
        params['utm_content'] = content
    
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    
    return urllib.parse.urlunparse(url_parts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UTM Link Builder")
    parser.add_argument("--url", required=True, help="Base URL")
    parser.add_argument("--source", required=True, help="UTM Source (e.g. facebook, google, newsletter)")
    parser.add_argument("--medium", required=True, help="UTM Medium (e.g. cpc, social, email)")
    parser.add_argument("--campaign", required=True, help="UTM Campaign name")
    parser.add_argument("--term", help="UTM Term (keywords)")
    parser.add_argument("--content", help="UTM Content (ad variant)")
    
    args = parser.parse_args()
    
    print(build_utm_url(args.url, args.source, args.medium, args.campaign, args.term, args.content))
