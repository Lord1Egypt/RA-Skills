#!/usr/bin/env python3
"""
Generate an interactive HTML map of Odoo contacts.
Usage:
  python3 generate_map.py [--city CITY]

The script reads ODOO_* from environment or a .env file next to the script.
"""
import xmlrpc.client, os, sys, time, argparse, requests, html

def load_env(path):
    env = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    return env

def get_config():
    # prefer process env, then .env in skill folder
    cfg = dict(os.environ)
    skill_env = os.path.join(os.path.dirname(__file__), '..', '.env')
    cfg.update({k:v for k,v in load_env(skill_env).items() if k not in cfg})
    return cfg

def authenticate(cfg):
    url = cfg.get('ODOO_URL')
    if not url:
        raise SystemExit('ODOO_URL not set')
    url = url.rstrip('/')
    db = cfg.get('ODOO_DB')
    username = cfg.get('ODOO_USERNAME')
    secret = cfg.get('ODOO_API_KEY') or cfg.get('ODOO_PASSWORD')
    if not (db and username and secret):
        raise SystemExit('Missing ODOO_DB / ODOO_USERNAME / ODOO_PASSWORD (or API key)')
    common = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/common')
    uid = common.authenticate(db, username, secret, {})
    if not uid:
        raise SystemExit('Authentication failed')
    models = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/object')
    return url, db, uid, secret, models

def geocode_address(q, headers):
    params = {'q': q, 'format': 'json', 'limit': 1, 'countrycodes': 'de'}
    r = requests.get('https://nominatim.openstreetmap.org/search', params=params, headers=headers, timeout=15)
    if r.status_code == 200:
        data = r.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    return None, None

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--city', help='Filter by city (ilike)')
    args = p.parse_args()

    cfg = get_config()
    url, db, uid, secret, models = authenticate(cfg)

    # determine country Germany id if possible
    try:
        country_ids = models.execute_kw(db, uid, secret, 'res.country', 'search', [[['code', '=', 'DE']]], {'limit': 1})
        country_id = country_ids[0] if country_ids else None
    except Exception:
        country_id = None

    if args.city:
        domain = [['city', 'ilike', args.city]]
    else:
        domain = [['country_id', '=', country_id]] if country_id else [['country_id', '!=', False]]

    fields = ['id', 'name', 'street', 'street2', 'zip', 'city', 'country_id', 'email', 'phone']
    partners = models.execute_kw(db, uid, secret, 'res.partner', 'search_read', [domain], {'fields': fields, 'limit': 10000})

    headers = {'User-Agent': 'OpenClaw/contact-map-bm/1.0'}
    entries = []
    for pidx, p in enumerate(partners, 1):
        parts = []
        if p.get('street'): parts.append(p.get('street'))
        if p.get('street2'): parts.append(p.get('street2'))
        if p.get('zip'): parts.append(p.get('zip'))
        if p.get('city'): parts.append(p.get('city'))
        addr = ', '.join([x for x in parts if x])
        # attempt to find coordinate-like custom fields
        lat = p.get('x_partner_lat') or p.get('x_lat') or p.get('latitude') or p.get('lat')
        lon = p.get('x_partner_lng') or p.get('x_lng') or p.get('longitude') or p.get('lng')
        if lat and lon:
            try:
                entries.append({'id': p['id'], 'name': p.get('name'), 'lat': float(lat), 'lon': float(lon), 'addr': addr, 'email': p.get('email'), 'phone': p.get('phone'), 'city': p.get('city')})
                continue
            except Exception:
                pass
        if addr:
            q = addr + ', Germany'
            latv, lonv = geocode_address(q, headers)
            if latv and lonv:
                entries.append({'id': p['id'], 'name': p.get('name'), 'lat': latv, 'lon': lonv, 'addr': addr, 'email': p.get('email'), 'phone': p.get('phone'), 'city': p.get('city')})
            # respect Nominatim rate limit
            time.sleep(1.1)

    # write HTML map
    outpath = os.path.join(os.path.expanduser('~'), '.openclaw', 'workspace', 'odoo_contacts_germany_map.html')
    # ensure path exists
    outpath = os.path.join(os.path.expanduser('~'), '.openclaw', 'workspace', 'odoo_contacts_germany_map.html')
    html_parts = []
    html_parts.append('<!doctype html>')
    html_parts.append('<html><head><meta charset="utf-8"/><title>Odoo Contacts Map</title>')
    html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_parts.append('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>')
    html_parts.append('<style>html,body,#map{height:100%;margin:0;padding:0}</style>')
    html_parts.append('</head><body><div id="map"></div>')
    html_parts.append('<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>')
    html_parts.append('<script>var map=L.map("map").setView([51.1657,10.4515],6);L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:19,attribution:"© OpenStreetMap contributors"}).addTo(map);var markers=L.layerGroup().addTo(map);')

    for e in entries:
        rec_url = f"{url}/web#id={e['id']}&model=res.partner&view_type=form"
        popup = f"<b>{html.escape(e['name'] or '')}</b><br/>{html.escape(e['addr'] or '')}"
        if e.get('email'): popup += '<br/>' + html.escape(e.get('email'))
        if e.get('phone'): popup += '<br/>' + html.escape(e.get('phone'))
        popup += f"<br/><a href='{rec_url}' target='_blank'>Open in Odoo</a>"
        popup_js = popup.replace("'", "\\'")
        html_parts.append(f"L.marker([{e['lat']},{e['lon']}]).addTo(markers).bindPopup('{popup_js}');")

    html_parts.append('if (markers.getLayers().length>0){var g=L.featureGroup(markers.getLayers());map.fitBounds(g.getBounds().pad(0.2));}')
    html_parts.append('</script></body></html>')

    outdir = os.path.join(os.path.expanduser('~'), '.openclaw', 'workspace')
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, 'odoo_contacts_germany_map.html')
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))
    print('MAP_WRITTEN', outfile, 'MARKERS', len(entries))

if __name__ == '__main__':
    main()
