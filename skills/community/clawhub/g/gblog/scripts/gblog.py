#!/usr/bin/env python3
"""
gblog - Blogger CLI
Manage Blogger posts via command line
"""

import os
import sys
import json
import argparse
import pickle
from pathlib import Path
from urllib.parse import urlencode, parse_qs
from urllib.request import Request, urlopen
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser

# Configuration
CONFIG_DIR = Path.home() / ".config" / "gblog"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
TOKEN_FILE = CONFIG_DIR / "token.json"
BLOGGER_API_BASE = "https://www.googleapis.com/blogger/v3"

class Colors:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"

def print_success(msg): print(f"{Colors.GREEN}✓{Colors.END} {msg}")
def print_info(msg): print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")
def print_warning(msg): print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")
def print_error(msg): print(f"{Colors.RED}✗{Colors.END} {msg}")

def load_credentials():
    """Load OAuth credentials from file"""
    if not CREDENTIALS_FILE.exists():
        print_error(f"Credentials not found at {CREDENTIALS_FILE}")
        print_info("Please save your Google OAuth credentials to ~/.config/gblog/credentials.json")
        sys.exit(1)
    
    with open(CREDENTIALS_FILE) as f:
        return json.load(f)

def load_token():
    """Load saved OAuth token"""
    if not TOKEN_FILE.exists():
        return None
    with open(TOKEN_FILE) as f:
        return json.load(f)

def save_token(token):
    """Save OAuth token"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token, f)
    os.chmod(TOKEN_FILE, 0o600)

def refresh_access_token():
    """Refresh access token using refresh token"""
    token = load_token()
    if not token or 'refresh_token' not in token:
        return None
    
    creds = load_credentials()
    client = creds.get('web', creds.get('installed', {}))
    
    data = urlencode({
        'client_id': client['client_id'],
        'client_secret': client['client_secret'],
        'refresh_token': token['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode()
    
    req = Request('https://oauth2.googleapis.com/token', data=data, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    
    try:
        response = urlopen(req)
        new_token = json.loads(response.read().decode())
        new_token['refresh_token'] = token['refresh_token']
        save_token(new_token)
        return new_token
    except Exception as e:
        print_error(f"Failed to refresh token: {e}")
        return None

def get_access_token():
    """Get valid access token"""
    token = load_token()
    if not token:
        print_error("Not authenticated. Run: gblog auth")
        sys.exit(1)
    
    # Try to use existing token
    access_token = token.get('access_token')
    
    # Test if token works
    req = Request(f"{BLOGGER_API_BASE}/users/self/blogs")
    req.add_header('Authorization', f'Bearer {access_token}')
    
    try:
        urlopen(req)
        return access_token
    except:
        # Token expired, try refresh
        new_token = refresh_access_token()
        if new_token:
            return new_token['access_token']
        print_error("Session expired. Run: gblog auth")
        sys.exit(1)

def api_request(endpoint, method='GET', data=None):
    """Make authenticated API request"""
    token = get_access_token()
    url = f"{BLOGGER_API_BASE}{endpoint}"
    
    req = Request(url, method=method)
    req.add_header('Authorization', f'Bearer {token}')
    
    if data:
        req.add_header('Content-Type', 'application/json')
        req.data = json.dumps(data).encode()
    
    try:
        response = urlopen(req)
        return json.loads(response.read().decode())
    except Exception as e:
        print_error(f"API request failed: {e}")
        raise

# Command implementations
def cmd_auth(args):
    """Authenticate with Google"""
    if args.status:
        token = load_token()
        if token:
            print_success("Authenticated")
            print_info(f"Token saved at: {TOKEN_FILE}")
        else:
            print_warning("Not authenticated")
        return
    
    if args.logout:
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()
        print_success("Logged out")
        return
    
    # Start OAuth flow
    creds = load_credentials()
    client = creds.get('web', creds.get('installed', {}))
    
    redirect_uri = "http://localhost:8085/oauth2callback"
    
    auth_params = {
        'client_id': client['client_id'],
        'redirect_uri': redirect_uri,
        'scope': 'https://www.googleapis.com/auth/blogger',
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent'
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(auth_params)}"
    
    print_info("Opening browser for authentication...")
    webbrowser.open(auth_url)
    
    # Start local server to receive callback
    code = None
    
    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal code
            if '/oauth2callback' in self.path:
                query = parse_qs(self.path.split('?')[1])
                code = query.get('code', [None])[0]
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html = (
                    '<html><body style="text-align:center;font-family:Arial;padding:50px;">'
                    '<h1 style="color:green;">Authentication Successful!</h1>'
                    '<p>You can close this window and return to the terminal.</p>'
                    '</body></html>'
                )
                self.wfile.write(html.encode('utf-8'))
    
    server = HTTPServer(('localhost', 8085), CallbackHandler)
    print_info("Waiting for authorization... (Ctrl+C to cancel)")
    
    while not code:
        server.handle_request()
    
    server.server_close()
    
    # Exchange code for token
    token_data = urlencode({
        'code': code,
        'client_id': client['client_id'],
        'client_secret': client['client_secret'],
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }).encode()
    
    req = Request('https://oauth2.googleapis.com/token', data=token_data, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    
    response = urlopen(req)
    token = json.loads(response.read().decode())
    save_token(token)
    
    print_success("Authentication successful!")
    print_info(f"Token saved to: {TOKEN_FILE}")

def cmd_list_blogs(args):
    """List user's blogs"""
    try:
        result = api_request("/users/self/blogs")
        blogs = result.get('items', [])
        
        if not blogs:
            print_warning("No blogs found")
            return
        
        print(f"\n{'ID':<25} {'Name':<30} {'Posts':<10}")
        print("-" * 65)
        for blog in blogs:
            print(f"{blog['id']:<25} {blog['name'][:29]:<30} {blog.get('posts', {}).get('totalItems', 0):<10}")
        print()
    except Exception as e:
        print_error(f"Failed to list blogs: {e}")

def cmd_list_posts(args):
    """List posts from a blog"""
    blog_id = args.blog_id or os.environ.get('GBLOG_DEFAULT_BLOG_ID')
    if not blog_id:
        print_error("Blog ID required. Use --blog-id or set GBLOG_DEFAULT_BLOG_ID")
        sys.exit(1)
    
    try:
        result = api_request(f"/blogs/{blog_id}/posts")
        posts = result.get('items', [])
        
        if not posts:
            print_warning("No posts found")
            return
        
        print(f"\n{'ID':<25} {'Date':<12} {'Status':<10} {'Title'}")
        print("-" * 80)
        for post in posts[:args.limit]:
            date = post['published'][:10]
            status = "DRAFT" if post.get('status') == 'DRAFT' else "LIVE"
            print(f"{post['id']:<25} {date:<12} {status:<10} {post['title'][:40]}")
        print()
    except Exception as e:
        print_error(f"Failed to list posts: {e}")

def cmd_post(args):
    """Create a new post"""
    blog_id = args.blog_id or os.environ.get('GBLOG_DEFAULT_BLOG_ID')
    if not blog_id:
        print_error("Blog ID required")
        sys.exit(1)
    
    # Read content
    if args.content:
        with open(args.content) as f:
            content = f.read()
    else:
        print_error("Content file required (--content)")
        sys.exit(1)
    
    post_data = {
        'kind': 'blogger#post',
        'title': args.title,
        'content': content
    }
    
    if args.labels:
        post_data['labels'] = [l.strip() for l in args.labels.split(',')]
    
    try:
        endpoint = f"/blogs/{blog_id}/posts"
        if args.draft:
            endpoint += "?isDraft=true"
        
        result = api_request(endpoint, method='POST', data=post_data)
        print_success(f"Post created: {result['url']}")
        print_info(f"Post ID: {result['id']}")
    except Exception as e:
        print_error(f"Failed to create post: {e}")

def cmd_edit(args):
    """Edit an existing post"""
    blog_id = args.blog_id or os.environ.get('GBLOG_DEFAULT_BLOG_ID')
    if not blog_id:
        print_error("Blog ID required")
        sys.exit(1)
    
    if not args.post_id:
        print_error("Post ID required (--post-id)")
        sys.exit(1)
    
    post_data = {}
    
    if args.title:
        post_data['title'] = args.title
    
    if args.content:
        with open(args.content) as f:
            post_data['content'] = f.read()
    
    if not post_data:
        print_error("Nothing to update. Use --title or --content")
        sys.exit(1)
    
    try:
        result = api_request(f"/blogs/{blog_id}/posts/{args.post_id}", 
                           method='PATCH', data=post_data)
        print_success(f"Post updated: {result['url']}")
    except Exception as e:
        print_error(f"Failed to update post: {e}")

def cmd_delete(args):
    """Delete a post"""
    blog_id = args.blog_id or os.environ.get('GBLOG_DEFAULT_BLOG_ID')
    if not blog_id or not args.post_id:
        print_error("Blog ID and Post ID required")
        sys.exit(1)
    
    if not args.yes:
        confirm = input(f"Delete post {args.post_id}? [y/N]: ")
        if confirm.lower() != 'y':
            print_info("Cancelled")
            return
    
    try:
        api_request(f"/blogs/{blog_id}/posts/{args.post_id}", method='DELETE')
        print_success("Post deleted")
    except Exception as e:
        print_error(f"Failed to delete post: {e}")

def cmd_get_post(args):
    """Get post details"""
    blog_id = args.blog_id or os.environ.get('GBLOG_DEFAULT_BLOG_ID')
    if not blog_id or not args.post_id:
        print_error("Blog ID and Post ID required")
        sys.exit(1)
    
    try:
        result = api_request(f"/blogs/{blog_id}/posts/{args.post_id}")
        print(f"\nTitle: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Published: {result['published']}")
        print(f"Updated: {result['updated']}")
        print(f"Status: {result.get('status', 'LIVE')}")
        if result.get('labels'):
            print(f"Labels: {', '.join(result['labels'])}")
        print(f"\nContent:\n{result['content'][:500]}...")
    except Exception as e:
        print_error(f"Failed to get post: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='gblog - Blogger CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  gblog auth                                    # Authenticate
  gblog list-blogs                              # List your blogs
  gblog list-posts --blog-id 12345              # List posts
  gblog post --blog-id 12345 --title "Hello" --content post.html
  gblog edit --blog-id 12345 --post-id 67890 --content updated.html
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Auth
    auth_parser = subparsers.add_parser('auth', help='Authenticate with Google')
    auth_parser.add_argument('--status', action='store_true', help='Check auth status')
    auth_parser.add_argument('--logout', action='store_true', help='Logout')
    
    # List blogs
    subparsers.add_parser('list-blogs', help='List your blogs')
    
    # List posts
    list_parser = subparsers.add_parser('list-posts', help='List posts from a blog')
    list_parser.add_argument('--blog-id', help='Blog ID')
    list_parser.add_argument('--limit', type=int, default=20, help='Number of posts')
    
    # Create post
    post_parser = subparsers.add_parser('post', help='Create a new post')
    post_parser.add_argument('--blog-id', help='Blog ID')
    post_parser.add_argument('--title', required=True, help='Post title')
    post_parser.add_argument('--content', required=True, help='HTML content file')
    post_parser.add_argument('--labels', help='Comma-separated labels')
    post_parser.add_argument('--draft', action='store_true', help='Save as draft')
    
    # Edit post
    edit_parser = subparsers.add_parser('edit', help='Edit a post')
    edit_parser.add_argument('--blog-id', help='Blog ID')
    edit_parser.add_argument('--post-id', required=True, help='Post ID')
    edit_parser.add_argument('--title', help='New title')
    edit_parser.add_argument('--content', help='New HTML content file')
    
    # Delete post
    delete_parser = subparsers.add_parser('delete', help='Delete a post')
    delete_parser.add_argument('--blog-id', help='Blog ID')
    delete_parser.add_argument('--post-id', required=True, help='Post ID')
    delete_parser.add_argument('--yes', action='store_true', help='Skip confirmation')
    
    # Get post
    get_parser = subparsers.add_parser('get-post', help='Get post details')
    get_parser.add_argument('--blog-id', help='Blog ID')
    get_parser.add_argument('--post-id', required=True, help='Post ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Route to command handler
    commands = {
        'auth': cmd_auth,
        'list-blogs': cmd_list_blogs,
        'list-posts': cmd_list_posts,
        'post': cmd_post,
        'edit': cmd_edit,
        'delete': cmd_delete,
        'get-post': cmd_get_post
    }
    
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
