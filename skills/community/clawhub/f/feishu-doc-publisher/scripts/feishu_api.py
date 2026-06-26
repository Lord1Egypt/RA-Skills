import urllib.request
import urllib.error
import json
import uuid

BASE_URL = 'https://open.feishu.cn/open-apis'

def _post_json(url, data, token=None, method='POST'):
    req = urllib.request.Request(url, method=method)
    req.add_header('Content-Type', 'application/json')
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    req.data = json.dumps(data).encode('utf-8')
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8')
        raise Exception(f"HTTPError {e.code}: {err_msg}")

def get_tenant_access_token(app_id, app_secret):
    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    data = {"app_id": app_id, "app_secret": app_secret}
    resp = _post_json(url, data)
    if resp.get('code') != 0:
        raise Exception(f"获取 token 失败: {resp.get('msg') or json.dumps(resp)}")
    return resp['tenant_access_token']

def convert_markdown_to_blocks(token, markdown_content):
    url = f"{BASE_URL}/docx/v1/documents/blocks/convert"
    data = {"content": markdown_content, "content_type": "markdown"}
    resp = _post_json(url, data, token)
    if resp.get('code') != 0:
        raise Exception(f"Markdown 转换失败: {resp.get('msg') or json.dumps(resp)}")
    return resp['data']

def create_document(token, title, folder_token=""):
    url = f"{BASE_URL}/docx/v1/documents"
    data = {"title": title, "folder_token": folder_token or ""}
    resp = _post_json(url, data, token)
    if resp.get('code') != 0:
        raise Exception(f"创建文档失败: {resp.get('msg') or json.dumps(resp)}")
    return resp['data']['document']['document_id']

def insert_descendant(token, document_id, block_id, children_id, descendants, index=None):
    url = f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/{block_id}/descendant"
    data = {"children_id": children_id, "descendants": descendants}
    if index is not None:
        data['index'] = index
    resp = _post_json(url, data, token)
    if resp.get('code') != 0:
        raise Exception(f"descendant 失败: code={resp.get('code')}, msg={resp.get('msg')}")
    return resp

def insert_children(token, document_id, block_id, blocks, index=None):
    url = f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/{block_id}/children"
    data = {"children": blocks}
    if index is not None:
        data['index'] = index
    resp = _post_json(url, data, token)
    if resp.get('code') != 0:
        raise Exception(f"children 失败: code={resp.get('code')}, msg={resp.get('msg')}")
    return resp

def upload_image_data(token, parent_node, file_info):
    url = f"{BASE_URL}/drive/v1/medias/upload_all"
    boundary = uuid.uuid4().hex
    
    body = []
    def add_field(name, value):
        body.append(f'--{boundary}\r\n')
        body.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n')
        body.append(f'{value}\r\n')

    add_field('file_name', file_info['fileName'])
    add_field('parent_type', 'docx_image')
    add_field('parent_node', parent_node)
    add_field('size', str(file_info['size']))
    
    body.append(f'--{boundary}\r\n')
    body.append(f'Content-Disposition: form-data; name="file"; filename="{file_info["fileName"]}"\r\n')
    body.append(f'Content-Type: {file_info["mimeType"]}\r\n\r\n')
    
    body_bytes = "".join(body).encode('utf-8')
    
    with open(file_info['path'], 'rb') as f:
        file_bytes = f.read()
        
    end_boundary = f'\r\n--{boundary}--\r\n'.encode('utf-8')
    final_data = body_bytes + file_bytes + end_boundary
    
    req = urllib.request.Request(url, method='POST')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    req.add_header('Authorization', f'Bearer {token}')
    req.data = final_data
    
    try:
        with urllib.request.urlopen(req) as response:
            resp = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8')
        raise Exception(f"HTTPError {e.code}: {err_msg}")
        
    if resp.get('code') != 0:
        raise Exception(f"上传图片失败: {resp.get('msg') or json.dumps(resp)}")
    return resp['data']['file_token']

def update_block_image(token, document_id, block_id, file_token):
    url = f"{BASE_URL}/docx/v1/documents/{document_id}/blocks/{block_id}"
    data = {"replace_image": {"token": file_token}}
    resp = _post_json(url, data, token, method='PATCH')
    if resp.get('code') != 0:
        raise Exception(f"更新图片块失败: {resp.get('msg') or json.dumps(resp)}")
    return resp

def update_public_permission(token, document_id, share_type):
    # 文档节点使用 drive/v1/permissions/:token/public 接口
    url = f"{BASE_URL}/drive/v1/permissions/{document_id}/public?type=docx"
    
    # 默认内网 (tenant)
    data = {
        "external_access": False,
        "security_entity": "anyone_can_view", 
        "comment_entity": "anyone_can_view",
        "share_entity": "same_tenant",
        "link_share_entity": share_type
    }
    
    if share_type.startswith("anyone"):
        data["external_access"] = True
        data["share_entity"] = "anyone"
        
    if share_type.endswith("editable"):
        data["security_entity"] = "anyone_can_edit"
        data["comment_entity"] = "anyone_can_edit"
        
    resp = _post_json(url, data, token, method='PATCH')
    if resp.get('code') != 0:
        raise Exception(f"更新文档权限失败 (请确认您的飞书应用是否拥有相应的 drive/v1/permissions 权限，以及企业后台策略是否允许配置该权限): {resp.get('msg') or json.dumps(resp)}")
    return resp

def transfer_document_owner(token, document_id, member_type, member_id):
    # 转移所有者
    url = f"{BASE_URL}/drive/v1/permissions/{document_id}/members/transfer_owner?type=docx&need_notification=true"
    data = {
        "member_type": member_type,
        "member_id": member_id
    }
    resp = _post_json(url, data, token, method='POST')
    if resp.get('code') != 0:
        raise Exception(f"转移所有权失败: {resp.get('msg') or json.dumps(resp)}")
    return resp
