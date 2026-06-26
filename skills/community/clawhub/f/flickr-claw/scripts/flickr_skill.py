import argparse
import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import sys

from requests_oauthlib import OAuth1Session

REQUEST_TOKEN_URL = 'https://www.flickr.com/services/oauth/request_token'
AUTHORIZE_URL = 'https://www.flickr.com/services/oauth/authorize'
ACCESS_TOKEN_URL = 'https://www.flickr.com/services/oauth/access_token'
REST_URL = 'https://api.flickr.com/services/rest'
CREDS_FILE = Path.home() / '.openclaw' / 'flickr-app-credentials.json'
DEFAULT_REQUEST_FILE = Path.home() / '.openclaw' / 'flickr-request-token-manual.txt'
DEFAULT_ACCESS_FILE = Path.home() / '.openclaw' / 'flickr-access-token-manual.txt'
DEFAULT_AUDIT_OUT = Path.cwd() / 'flickr_recent_uploads_audit.csv'
DEFAULT_DOWNLOAD_DIR = Path.cwd() / 'flickr-latest-downloads'
DEFAULT_ALBUM_OUT = Path.cwd() / 'flickr_album_photos.csv'


def safe_print(message: str):
    try:
        print(message)
    except UnicodeEncodeError:
        encoded = message.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8', errors='replace')
        print(encoded)


def fail(message: str):
    raise SystemExit(message)


def load_creds(creds_file: Path = CREDS_FILE):
    if not creds_file.exists():
        fail(
            f'Missing Flickr credentials file: {creds_file}\n'
            'Create ~/.openclaw/flickr-app-credentials.json with api_key and api_secret.'
        )
    try:
        data = json.loads(creds_file.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        fail(f'Could not parse credentials file as JSON: {creds_file}\n{e}')
    api_key = data.get('api_key')
    api_secret = data.get('api_secret')
    if not api_key or not api_secret:
        fail(f'Credentials file must contain api_key and api_secret: {creds_file}')
    return api_key, api_secret


def parse_tokens(path: Path):
    if not path.exists():
        fail(
            f'Missing token file: {path}\n'
            'Run --start-auth, approve the Flickr auth URL, then run --finish-auth --verifier CODE.'
        )
    data = path.read_text(encoding='utf-8').strip()
    if data.startswith('{') and data.endswith('}'):
        items = {}
        inner = data[1:-1].strip()
        for part in inner.split(','):
            if ':' not in part:
                continue
            k, v = part.split(':', 1)
            items[k.strip().strip("'\"")] = v.strip().strip("'\"")
        if not items.get('oauth_token') or not items.get('oauth_token_secret'):
            fail(f'Token file is missing oauth_token or oauth_token_secret: {path}')
        return items
    fail(f'Could not parse token file: {path}')


def make_oauth(access_file: Path):
    api_key, api_secret = load_creds()
    at = parse_tokens(access_file)
    return OAuth1Session(
        api_key,
        client_secret=api_secret,
        resource_owner_key=at['oauth_token'],
        resource_owner_secret=at['oauth_token_secret'],
    )


def start_auth(req_file: Path, perms: str = 'write'):
    api_key, api_secret = load_creds()
    oauth = OAuth1Session(api_key, client_secret=api_secret, callback_uri='oob')
    tokens = oauth.fetch_request_token(REQUEST_TOKEN_URL)
    req_file.parent.mkdir(parents=True, exist_ok=True)
    req_file.write_text(str(tokens), encoding='utf-8')
    auth_url = oauth.authorization_url(AUTHORIZE_URL, perms=perms)
    print('AUTH_URL:' + auth_url)
    print('REQUEST_TOKEN_FILE:' + str(req_file))
    print('REQUEST_PERMS:' + perms)


def finish_auth(req_file: Path, verifier: str, access_file: Path):
    api_key, api_secret = load_creds()
    rt = parse_tokens(req_file)
    oauth = OAuth1Session(
        api_key,
        client_secret=api_secret,
        resource_owner_key=rt['oauth_token'],
        resource_owner_secret=rt['oauth_token_secret'],
        verifier=verifier,
    )
    try:
        tokens = oauth.fetch_access_token(ACCESS_TOKEN_URL)
    except Exception as e:
        fail(
            'Could not redeem Flickr verifier code.\n'
            'Make sure you used the most recent auth URL, approved it, and pasted the verifier exactly.\n'
            f'Details: {e}'
        )
    access_file.parent.mkdir(parents=True, exist_ok=True)
    access_file.write_text(str(tokens), encoding='utf-8')
    print('ACCESS_TOKEN_FILE:' + str(access_file))


def check_auth(access_file: Path):
    oauth = make_oauth(access_file)
    info = flickr_get(oauth, 'flickr.test.login')
    user = info.get('user', {})
    print('AUTH_OK')
    print('USER_ID:' + str(user.get('id', '')))
    print('USERNAME:' + str((user.get('username') or {}).get('_content', '')))
    print('CHECK_AUTH_NOTE: This confirms the token works for authenticated Flickr API calls. Write permission still depends on how the token was minted.')


def flickr_get(oauth, method, **params):
    q = {'method': method, 'format': 'json', 'nojsoncallback': '1'}
    q.update(params)
    r = oauth.get(REST_URL, params=q, timeout=60)
    r.raise_for_status()
    data = r.json()
    if data.get('stat') != 'ok':
        raise RuntimeError(f'Flickr API error for {method}: {data}')
    return data


def flickr_post(oauth, method, **params):
    form = {'method': method, 'format': 'json', 'nojsoncallback': '1'}
    form.update(params)
    r = oauth.post(REST_URL, data=form, timeout=60)
    r.raise_for_status()
    data = r.json()
    if data.get('stat') != 'ok':
        raise RuntimeError(f'Flickr API error for {method}: {data}')
    return data


def photo_row_from_api_photo(p):
    pid = p['id']
    title = p.get('title', '') or ''
    desc = (p.get('description') or {}).get('_content', '') if isinstance(p.get('description'), dict) else ''
    tags = p.get('tags', '') or ''
    geotag = ('latitude' in p and p.get('latitude') not in ('0', '0.0', None, '')) or ('longitude' in p and p.get('longitude') not in ('0', '0.0', None, ''))
    taken = p.get('datetaken', '')
    uploaded = p.get('dateupload', '')
    url = f"https://www.flickr.com/photos/{p.get('pathalias') or 'me'}/{pid}"
    return {
        'photo_id': pid,
        'title': title,
        'description_present': 'yes' if desc.strip() else 'no',
        'tag_count': len([t for t in tags.split(' ') if t.strip()]) if tags else 0,
        'tags': tags,
        'uploaded_at': uploaded,
        'taken_at': taken,
        'has_geo': 'yes' if geotag else 'no',
        'photo_url': url,
    }


def get_authenticated_user_id(oauth):
    info = flickr_get(oauth, 'flickr.test.login')
    user = info.get('user', {})
    user_id = user.get('id')
    if not user_id:
        fail('Could not resolve authenticated Flickr user ID.')
    return user_id


def rows_from_recent(oauth, days: int):
    min_upload_date = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp())
    user_id = get_authenticated_user_id(oauth)
    page = 1
    rows = []
    while True:
        data = flickr_get(
            oauth,
            'flickr.people.getPhotos',
            user_id=user_id,
            min_upload_date=str(min_upload_date),
            extras='date_upload,date_taken,tags,geo,description,path_alias',
            per_page='500',
            page=str(page),
        )
        photos = data['photos']
        for p in photos['photo']:
            rows.append(photo_row_from_api_photo(p))
        if page >= int(photos['pages']):
            break
        page += 1
    return rows


def write_csv(rows, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['photo_id', 'title', 'description_present', 'tag_count', 'tags', 'uploaded_at', 'taken_at', 'has_geo', 'photo_url'])
        writer.writeheader()
        writer.writerows(rows)
    print('WROTE:' + str(out))
    print('ROWS:' + str(len(rows)))


def audit(access_file: Path, days: int, out: Path):
    oauth = make_oauth(access_file)
    rows = rows_from_recent(oauth, days)
    write_csv(rows, out)


def list_albums(access_file: Path):
    oauth = make_oauth(access_file)
    user_id = get_authenticated_user_id(oauth)
    page = 1
    count = 0
    while True:
        data = flickr_get(oauth, 'flickr.photosets.getList', user_id=user_id, page=str(page), per_page='500')
        photosets = data['photosets']
        for s in photosets.get('photoset', []):
            count += 1
            title = ((s.get('title') or {}).get('_content', '')).strip()
            safe_print(f"ALBUM:{s.get('id','')}\t{title}\tPHOTOS:{s.get('photos','')}")
        if page >= int(photosets.get('pages', 1)):
            break
        page += 1
    safe_print('ALBUM_COUNT:' + str(count))


def rows_from_album(oauth, album_id: str):
    page = 1
    rows = []
    while True:
        data = flickr_get(
            oauth,
            'flickr.photosets.getPhotos',
            photoset_id=album_id,
            extras='date_upload,date_taken,tags,geo,description,path_alias',
            per_page='500',
            page=str(page),
        )
        photoset = data['photoset']
        for p in photoset.get('photo', []):
            rows.append(photo_row_from_api_photo(p))
        if page >= int(photoset.get('pages', 1)):
            break
        page += 1
    return rows


def album_photos(access_file: Path, album_id: str, out: Path):
    oauth = make_oauth(access_file)
    rows = rows_from_album(oauth, album_id)
    write_csv(rows, out)


def quote_tags(tags_list):
    return ' '.join(f'"{t}"' if ' ' in t else t for t in tags_list)


def add_tags(access_file: Path, photo_id: str, tags: str):
    oauth = make_oauth(access_file)
    info = flickr_get(oauth, 'flickr.photos.getInfo', photo_id=photo_id)
    existing_raw = ((info.get('photo') or {}).get('tags') or {}).get('tag', [])
    existing = [t.get('raw', '').strip() for t in existing_raw if t.get('raw', '').strip()]
    additions = [t.strip() for t in tags.split(',') if t.strip()]
    merged = []
    seen = set()
    for tag in existing + additions:
        key = tag.lower()
        if key in seen:
            continue
        seen.add(key)
        merged.append(tag)
    try:
        flickr_post(oauth, 'flickr.photos.setTags', photo_id=photo_id, tags=quote_tags(merged))
    except Exception as e:
        fail(
            'Could not add tags.\n'
            'If the token was authorized with read-only access, mint a new write token with --start-auth --perms write.\n'
            f'Details: {e}'
        )
    print('ADD_TAGS_OK:' + photo_id)
    print('FINAL:' + ', '.join(merged))


def set_tags(access_file: Path, photo_id: str, tags: str):
    oauth = make_oauth(access_file)
    try:
        flickr_post(oauth, 'flickr.photos.setTags', photo_id=photo_id, tags=tags)
    except Exception as e:
        fail(
            'Could not replace tags.\n'
            'If the token was authorized with read-only access, mint a new write token with --start-auth --perms write.\n'
            f'Details: {e}'
        )
    print('SET_TAGS_OK:' + photo_id)
    print('TAGS:' + tags)


def set_title(access_file: Path, photo_id: str, title: str):
    oauth = make_oauth(access_file)
    try:
        flickr_post(oauth, 'flickr.photos.setMeta', photo_id=photo_id, title=title)
    except Exception as e:
        fail(
            'Could not set title.\n'
            'This operation needs a write-capable token.\n'
            f'Details: {e}'
        )
    print('SET_TITLE_OK:' + photo_id)
    print('TITLE:' + title)


def set_description(access_file: Path, photo_id: str, description: str):
    oauth = make_oauth(access_file)
    info = flickr_get(oauth, 'flickr.photos.getInfo', photo_id=photo_id)
    current_title = ((info.get('photo') or {}).get('title') or {}).get('_content', '')
    try:
        flickr_post(oauth, 'flickr.photos.setMeta', photo_id=photo_id, title=current_title, description=description)
    except Exception as e:
        fail(
            'Could not set description.\n'
            'This operation needs a write-capable token.\n'
            f'Details: {e}'
        )
    print('SET_DESCRIPTION_OK:' + photo_id)


def set_meta(access_file: Path, photo_id: str, title: str, description: str):
    oauth = make_oauth(access_file)
    try:
        flickr_post(oauth, 'flickr.photos.setMeta', photo_id=photo_id, title=title, description=description)
    except Exception as e:
        fail(
            'Could not set title and description.\n'
            'This operation needs a write-capable token.\n'
            f'Details: {e}'
        )
    print('SET_META_OK:' + photo_id)


def pick_size(sizes):
    preferred = ['Large 2048', 'Large 1600', 'Large', 'Medium 1024', 'Medium 800', 'Medium 640', 'Medium']
    by_label = {s['label']: s for s in sizes}
    for label in preferred:
        if label in by_label:
            return by_label[label]
    return sizes[-1]


def download_photo_rows(oauth, rows, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for i, row in enumerate(rows, start=1):
        pid = row['photo_id']
        sizes = flickr_get(oauth, 'flickr.photos.getSizes', photo_id=pid)['sizes']['size']
        chosen = pick_size(sizes)
        url = chosen['source']
        ext = Path(url).suffix or '.jpg'
        out = out_dir / f"{i:02d}_{pid}{ext}"
        img = oauth.get(url, timeout=120)
        img.raise_for_status()
        out.write_bytes(img.content)
        row = dict(row)
        row['downloaded_file'] = str(out)
        row['download_label'] = chosen.get('label')
        row['width'] = chosen.get('width')
        row['height'] = chosen.get('height')
        manifest.append(row)
        print('DOWNLOADED:' + str(out))
    manifest_path = out_dir / 'manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('MANIFEST:' + str(manifest_path))


def download_latest(access_file: Path, count: int, days: int, out_dir: Path):
    oauth = make_oauth(access_file)
    rows = rows_from_recent(oauth, days)
    latest = sorted(rows, key=lambda r: int(r['uploaded_at'] or '0'), reverse=True)[:count]
    download_photo_rows(oauth, latest, out_dir)


def download_album(access_file: Path, album_id: str, out_dir: Path):
    oauth = make_oauth(access_file)
    rows = rows_from_album(oauth, album_id)
    download_photo_rows(oauth, rows, out_dir)


def main():
    ap = argparse.ArgumentParser(
        description='Authenticate to Flickr, export metadata, download recent or album images locally, and edit tags, titles, and descriptions.'
    )
    ap.add_argument('--request-file', default=str(DEFAULT_REQUEST_FILE), help='Path to the saved Flickr request-token file.')
    ap.add_argument('--access-file', default=str(DEFAULT_ACCESS_FILE), help='Path to the saved Flickr access-token file.')
    ap.add_argument('--start-auth', action='store_true', help='Start Flickr OAuth and print an authorization URL.')
    ap.add_argument('--finish-auth', action='store_true', help='Redeem a Flickr verifier code and save the access token.')
    ap.add_argument('--audit', action='store_true', help='Export recent Flickr uploads to CSV.')
    ap.add_argument('--check-auth', action='store_true', help='Verify that the current token works for authenticated Flickr API calls.')
    ap.add_argument('--list-albums', action='store_true', help='List albums/photosets for the authenticated Flickr account.')
    ap.add_argument('--album-photos', action='store_true', help='Export photos from one album/photoset to CSV.')
    ap.add_argument('--download-latest', action='store_true', help='Download the latest recent photos for local review.')
    ap.add_argument('--download-album', action='store_true', help='Download all photos from one album/photoset for local review.')
    ap.add_argument('--set-tags', action='store_true', help='Replace the full tag list on a photo.')
    ap.add_argument('--add-tags', action='store_true', help='Merge new tags into the existing tag list on a photo.')
    ap.add_argument('--set-title', action='store_true', help='Set the title on a photo.')
    ap.add_argument('--set-description', action='store_true', help='Set the description on a photo.')
    ap.add_argument('--set-meta', action='store_true', help='Set both title and description on a photo.')
    ap.add_argument('--photo-id', help='Flickr photo ID for metadata write operations.')
    ap.add_argument('--album-id', help='Flickr album/photoset ID for album export or download operations.')
    ap.add_argument('--tags', help='Comma-separated tags for --add-tags, or a full tag string for --set-tags.')
    ap.add_argument('--title', help='Photo title for --set-title or --set-meta.')
    ap.add_argument('--description', help='Photo description for --set-description or --set-meta.')
    ap.add_argument('--verifier', help='Verifier code returned by Flickr after approval.')
    ap.add_argument('--perms', choices=['read', 'write', 'delete'], default='write', help='Requested Flickr OAuth permission level.')
    ap.add_argument('--days', type=int, default=30, help='How many recent days to inspect for audit or download operations.')
    ap.add_argument('--count', type=int, default=10, help='How many recent photos to download with --download-latest.')
    ap.add_argument('--out', default=str(DEFAULT_AUDIT_OUT), help='CSV output path for --audit or --album-photos.')
    ap.add_argument('--out-dir', default=str(DEFAULT_DOWNLOAD_DIR), help='Output directory for --download-latest or --download-album.')
    args = ap.parse_args()
    req = Path(args.request_file)
    acc = Path(args.access_file)
    if args.start_auth:
        start_auth(req, args.perms)
    elif args.finish_auth:
        if not args.verifier:
            fail('Missing --verifier')
        finish_auth(req, args.verifier, acc)
    elif args.audit:
        audit(acc, args.days, Path(args.out))
    elif args.check_auth:
        check_auth(acc)
    elif args.list_albums:
        list_albums(acc)
    elif args.album_photos:
        if not args.album_id:
            fail('Need --album-id')
        album_photos(acc, args.album_id, Path(args.out))
    elif args.download_latest:
        download_latest(acc, args.count, args.days, Path(args.out_dir))
    elif args.download_album:
        if not args.album_id:
            fail('Need --album-id')
        download_album(acc, args.album_id, Path(args.out_dir))
    elif args.set_tags:
        if not args.photo_id or not args.tags:
            fail('Need --photo-id and --tags')
        set_tags(acc, args.photo_id, args.tags)
    elif args.add_tags:
        if not args.photo_id or not args.tags:
            fail('Need --photo-id and --tags')
        add_tags(acc, args.photo_id, args.tags)
    elif args.set_title:
        if not args.photo_id or args.title is None:
            fail('Need --photo-id and --title')
        set_title(acc, args.photo_id, args.title)
    elif args.set_description:
        if not args.photo_id or args.description is None:
            fail('Need --photo-id and --description')
        set_description(acc, args.photo_id, args.description)
    elif args.set_meta:
        if not args.photo_id or args.title is None or args.description is None:
            fail('Need --photo-id, --title, and --description')
        set_meta(acc, args.photo_id, args.title, args.description)
    else:
        fail('Use one of --start-auth --finish-auth --audit --check-auth --list-albums --album-photos --download-latest --download-album --set-tags --add-tags --set-title --set-description --set-meta')


if __name__ == '__main__':
    main()
