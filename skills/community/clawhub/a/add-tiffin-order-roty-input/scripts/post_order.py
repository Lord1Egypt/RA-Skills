import json
import urllib.request
import urllib.error

ENDPOINT = 'https://newdailyorderandcartcreation-818352713629.australia-southeast1.run.app'


def post_order(payload, timeout=30):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(ENDPOINT, data=data, method='POST')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            body = resp.read().decode('utf-8')
            try:
                body_json = json.loads(body)
            except Exception:
                body_json = body
            return status, body_json
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode('utf-8')
            body_json = json.loads(body)
        except Exception:
            body_json = e.reason
        return e.code, body_json
    except Exception as e:
        return 0, str(e)

if __name__ == '__main__':
    print('post_order helper (urllib)')
