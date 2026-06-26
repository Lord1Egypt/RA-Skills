import click
from cdn_client import init_cdn_client
from config import get_recommended_config
import json

@click.group()
def cli():
    """BytePlus CDN CLI Tool"""
    pass

def build_origin_config(instance_type, origin_address, is_private=False, auth_type=None, ak=None, sk=None, region=None):
    origin_line = {
        "OriginType": "primary",
        "InstanceType": instance_type,
        "Address": origin_address,
        "HttpPort": "80",
        "HttpsPort": "443",
        "Weight": "1"
    }
    
    if region:
        origin_line["Region"] = region
    
    if instance_type == "tos":
        origin_line["PrivateBucketAccess"] = is_private
        
        # 兼容性处理：如果明确是第三方厂商存储桶 (oss/cos/aws_common)，则强制为第三方存储桶启用鉴权配置，即使它不是私有桶
        # BytePlus CDN 对 tos 类型的外部存储桶处理逻辑较为特殊
        if auth_type and auth_type != "tos":
            origin_line["BucketSource"] = auth_type
            
        if auth_type and auth_type != "tos":
            # 无论是否私有，只要是第三方 bucket，都必须配置 PrivateBucketAuth。如果是公开桶，设置 Switch 为 False 即可。
            auth_info = {
                "Switch": is_private,
                "AuthType": auth_type
            }
            if is_private and ak and sk:
                auth_info["TosAuthInformation"] = {
                    "AccessKeyId": ak,
                    "AccessKeySecret": sk
                }
                if region:
                    auth_info["TosAuthInformation"]["Region"] = region
            origin_line["PrivateBucketAuth"] = auth_info
        elif is_private and auth_type == "tos":
            origin_line["PrivateBucketAuth"] = {
                "Switch": True,
                "AuthType": "tos"
            }
            
    return {
        "OriginAction": {
            "OriginLines": [origin_line]
        }
    }

def get_missing_auth_params(is_private, auth_type, ak, sk, region):
    if is_private and auth_type and auth_type != "tos":
        if not ak:
            ak = click.prompt('Please enter Bucket Access Key (AK)', default='')
        if not sk:
            sk = click.prompt('Please enter Bucket Secret Key (SK)', hide_input=True, default='')
        if auth_type == 'aws_common' and not region:
            region = click.prompt('Please enter AWS Region (e.g., us-east-1)', default='')
    return ak, sk, region

def handle_add_domain(domain, origin, service_type, project, apply_recommended, instance_type, is_private=False, auth_type=None, ak=None, sk=None, region=None):
    ak, sk, region = get_missing_auth_params(is_private, auth_type, ak, sk, region)
    client = init_cdn_client()
    body = {
        "Domain": domain,
        "ServiceType": service_type,
        "Project": project,
        "ServiceRegion": "outside_chinese_mainland",
        "OriginProtocol": "https" if instance_type == "tos" else "http",
        "Origin": [build_origin_config(instance_type, origin, is_private, auth_type, ak, sk, region)]
    }
    
    if apply_recommended == "yes":
        rec_config = get_recommended_config(service_type)
        body.update(rec_config)
        
    try:
        resp = client.add_cdn_domain(body)
        click.echo(f"Success: {json.dumps(resp, indent=2)}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.group()
def add_domain():
    """Add a new CDN domain."""
    pass

def common_add_domain_options(f):
    f = click.option('--domain', prompt='Please enter the domain to add', help='The domain to add')(f)
    f = click.option('--origin', prompt='Please enter the origin address (e.g. 1.1.1.1 or bucket domain)', help='Origin address')(f)
    f = click.option('--service-type', prompt='Please select service type', type=click.Choice(['web', 'download', 'video']), help='Service type')(f)
    f = click.option('--project', default='default', help='BytePlus project')(f)
    f = click.option('--apply-recommended', prompt='Apply recommended configurations?', type=click.Choice(['yes', 'no']), default='no', help='Apply recommended configuration')(f)
    return f

def bucket_options(f):
    f = click.option('--private-bucket', prompt='Is this a private bucket?', type=click.Choice(['yes', 'no']), default='no', help='Is private bucket')(f)
    f = click.option('--bucket-ak', default='', help='Bucket Access Key (required if private)')(f)
    f = click.option('--bucket-sk', default='', help='Bucket Secret Key (required if private)')(f)
    return f

@add_domain.command('oss')
@common_add_domain_options
@bucket_options
def add_domain_oss(domain, origin, service_type, project, apply_recommended, private_bucket, bucket_ak, bucket_sk):
    """Add domain with Aliyun OSS origin"""
    is_private = (private_bucket == 'yes')
    handle_add_domain(domain, origin, service_type, project, apply_recommended, 'tos', is_private, 'oss', bucket_ak, bucket_sk)

@add_domain.command('cos')
@common_add_domain_options
@bucket_options
def add_domain_cos(domain, origin, service_type, project, apply_recommended, private_bucket, bucket_ak, bucket_sk):
    """Add domain with Tencent COS origin"""
    is_private = (private_bucket == 'yes')
    handle_add_domain(domain, origin, service_type, project, apply_recommended, 'tos', is_private, 'cos', bucket_ak, bucket_sk)

@add_domain.command('aws')
@common_add_domain_options
@bucket_options
@click.option('--region', help='AWS Region (required if private)')
def add_domain_aws(domain, origin, service_type, project, apply_recommended, private_bucket, bucket_ak, bucket_sk, region):
    """Add domain with AWS S3 origin"""
    is_private = (private_bucket == 'yes')
    handle_add_domain(domain, origin, service_type, project, apply_recommended, 'tos', is_private, 'aws_common', bucket_ak, bucket_sk, region)

@add_domain.command('tos')
@common_add_domain_options
@click.option('--private-bucket', type=click.Choice(['yes', 'no']), default='no', help='Is private bucket')
def add_domain_tos(domain, origin, service_type, project, apply_recommended, private_bucket):
    """Add domain with BytePlus TOS origin"""
    is_private = (private_bucket == 'yes')
    handle_add_domain(domain, origin, service_type, project, apply_recommended, 'tos', is_private, 'tos')

@add_domain.command('ip')
@common_add_domain_options
def add_domain_ip(domain, origin, service_type, project, apply_recommended):
    """Add domain with IP origin"""
    handle_add_domain(domain, origin, service_type, project, apply_recommended, 'ip')

@add_domain.command('domain')
@common_add_domain_options
def add_domain_domain(domain, origin, service_type, project, apply_recommended):
    """Add domain with Domain origin"""
    handle_add_domain(domain, origin, service_type, project, apply_recommended, 'domain')

def handle_add_template_domain(domain, service_template_id, cipher_template_id=None, https_switch='off', cert_id=None, project='default', service_region='outside_chinese_mainland', rule_template_ids=None):
    client = init_cdn_client()
    body = {
        "Domain": domain,
        "ServiceTemplateId": service_template_id,
        "HTTPSSwitch": https_switch,
        "Project": project,
        "ServiceRegion": service_region
    }
    
    if cipher_template_id:
        body["CipherTemplateId"] = cipher_template_id
    if cert_id:
        body["CertId"] = cert_id
    if rule_template_ids:
        body["RuleTemplateIds"] = rule_template_ids
    
    try:
        if hasattr(client, 'add_template_domain'):
            res = client.add_template_domain(body)
        else:
            from byteplus_sdk.cdn.service import ApiInfo
            client.api_info['AddTemplateDomain'] = ApiInfo(
                "POST", "/", {"Action": "AddTemplateDomain", "Version": "2021-03-01"}, {}, {"Content-Type": "application/json"}
            )
            res = client.json('AddTemplateDomain', {}, body)
            if isinstance(res, bytes):
                res = json.loads(res.decode('utf-8'))
            
            if isinstance(res, str):
                res_dict = json.loads(res)
            else:
                res_dict = res
            
            if "ResponseMetadata" in res_dict and "Error" in res_dict["ResponseMetadata"]:
                error_info = res_dict["ResponseMetadata"]["Error"]
                raise Exception(f"{error_info.get('Code')}: {error_info.get('Message')}")
                
        click.echo(f"Success: {json.dumps(res, indent=2)}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@add_domain.command('template')
@click.option('--domain', required=True, prompt='Please enter domain(s) (comma separated, max 50)', help='Domain(s) to add')
@click.option('--service-template-id', required=True, prompt='Please enter Service Template ID', help='Service Template ID')
@click.option('--cipher-template-id', help='Cipher Template ID')
@click.option('--https-switch', type=click.Choice(['on', 'off']), default='off', prompt='Enable HTTPS? (on/off)', help='Enable HTTPS service')
@click.option('--cert-id', help='Certificate ID (required if HTTPS is on)')
@click.option('--project', default='default', help='BytePlus project')
@click.option('--service-region', type=click.Choice(['outside_chinese_mainland', 'chinese_mainland', 'global']), default='outside_chinese_mainland', help='Service region')
@click.option('--rule-template-ids', help='Rule Template IDs (comma separated)')
def add_domain_template(domain, service_template_id, cipher_template_id, https_switch, cert_id, project, service_region, rule_template_ids):
    """Add domain by binding existing service template"""
    rule_ids = None
    if rule_template_ids:
        rule_ids = [r.strip() for r in rule_template_ids.split(',') if r.strip()]
    
    handle_add_template_domain(
        domain,
        service_template_id,
        cipher_template_id=cipher_template_id,
        https_switch=https_switch,
        cert_id=cert_id,
        project=project,
        service_region=service_region,
        rule_template_ids=rule_ids
    )

def handle_create_template(title, message, origin, service_type, project, apply_recommended, instance_type, is_private=False, auth_type=None, ak=None, sk=None, region=None):
    ak, sk, region = get_missing_auth_params(is_private, auth_type, ak, sk, region)
    client = init_cdn_client()
    body = {
        "Title": title,
        "Message": message or "",
        "Project": project,
        "OriginProtocol": "https" if instance_type == "tos" else "http",
        "Origin": [build_origin_config(instance_type, origin, is_private, auth_type, ak, sk, region)]
    }
    
    if apply_recommended == "yes":
        rec_config = get_recommended_config(service_type)
        body.update(rec_config)
        
    try:
        resp = client.create_service_template(body)
        click.echo(f"Success: {json.dumps(resp, indent=2)}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.group()
def create_template():
    """Create CDN service template."""
    pass

def common_template_options(f):
    f = click.option('--title', required=True, help='Template title')(f)
    f = click.option('--message', help='Template description message')(f)
    f = click.option('--origin', required=True, help='Origin address')(f)
    f = click.option('--service-type', type=click.Choice(['web', 'download', 'video']), required=True, help='Service type')(f)
    f = click.option('--project', default='default', help='BytePlus project')(f)
    f = click.option('--apply-recommended', type=click.Choice(['yes', 'no']), default='no', help='Apply recommended configuration')(f)
    return f

@create_template.command('oss')
@common_template_options
@bucket_options
def create_template_oss(title, message, origin, service_type, project, apply_recommended, private_bucket, bucket_ak, bucket_sk):
    """Create template with Aliyun OSS origin"""
    is_private = (private_bucket == 'yes')
    handle_create_template(title, message, origin, service_type, project, apply_recommended, 'tos', is_private, 'oss', bucket_ak, bucket_sk)

@create_template.command('cos')
@common_template_options
@bucket_options
def create_template_cos(title, message, origin, service_type, project, apply_recommended, private_bucket, bucket_ak, bucket_sk):
    """Create template with Tencent COS origin"""
    is_private = (private_bucket == 'yes')
    handle_create_template(title, message, origin, service_type, project, apply_recommended, 'tos', is_private, 'cos', bucket_ak, bucket_sk)

@create_template.command('aws')
@common_template_options
@bucket_options
@click.option('--region', help='AWS Region (required if private)')
def create_template_aws(title, message, origin, service_type, project, apply_recommended, private_bucket, bucket_ak, bucket_sk, region):
    """Create template with AWS S3 origin"""
    is_private = (private_bucket == 'yes')
    handle_create_template(title, message, origin, service_type, project, apply_recommended, 'tos', is_private, 'aws_common', bucket_ak, bucket_sk, region)

@create_template.command('ip')
@common_template_options
def create_template_ip(title, message, origin, service_type, project, apply_recommended):
    """Create template with IP origin"""
    handle_create_template(title, message, origin, service_type, project, apply_recommended, 'ip')

@create_template.command('domain')
@common_template_options
def create_template_domain(title, message, origin, service_type, project, apply_recommended):
    """Create template with Domain origin"""
    handle_create_template(title, message, origin, service_type, project, apply_recommended, 'domain')

@cli.group()
def refresh():
    """Submit refresh task."""
    pass

@refresh.command('file')
@click.option('--urls', required=True, help='Comma separated URLs to refresh (max 100)')
def refresh_file(urls):
    """Refresh file URLs"""
    client = init_cdn_client()
    url_list = [u.strip() for u in urls.split(',') if u.strip()]
    if len(url_list) > 100:
        click.echo("Error: Max 100 URLs allowed for file refresh", err=True)
        return
        
    body = {
        "Type": "file",
        "UrlList": url_list
    }
    try:
        resp = client.submit_refresh_task(body)
        click.echo(f"Success: {json.dumps(resp, indent=2)}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@refresh.command('dir')
@click.option('--urls', required=True, help='Comma separated Directory URLs to refresh (max 50)')
def refresh_dir(urls):
    """Refresh directory URLs"""
    client = init_cdn_client()
    url_list = [u.strip() for u in urls.split(',') if u.strip()]
    if len(url_list) > 50:
        click.echo("Error: Max 50 URLs allowed for dir refresh", err=True)
        return
        
    body = {
        "Type": "dir",
        "UrlList": url_list
    }
    try:
        resp = client.submit_refresh_task(body)
        click.echo(f"Success: {json.dumps(resp, indent=2)}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.command('preload')
@click.option('--urls', required=True, help='Comma separated URLs to preload (max 100)')
def preload_file(urls):
    """Submit preload task"""
    client = init_cdn_client()
    url_list = [u.strip() for u in urls.split(',') if u.strip()]
    if len(url_list) > 100:
        click.echo("Error: Max 100 URLs allowed for preload", err=True)
        return
        
    body = {
        "UrlList": url_list
    }
    try:
        resp = client.submit_preload_task(body)
        click.echo(f"Success: {json.dumps(resp, indent=2)}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.group()
def log_offline():
    """Create an offline log store task."""
    pass

def common_offline_options(f):
    f = click.option('--bucket', required=True, prompt='Please enter Bucket path (e.g. my-bucket/logs)', help='Bucket path for offline logs')(f)
    f = click.option('--domain', required=True, prompt='Please enter associated domains (comma separated, or use "all" for all domains)', help='Associated domains')(f)
    return f

def handle_log_offline(bucket, domain, endpoint, region, task_type, is_private=False, ak=None, sk=None):
    if domain.lower() == 'all':
        domain = '*'
        
    client = init_cdn_client()
    body = {
        "Bucket": bucket,
        "Domain": domain,
        "TaskType": task_type,
        "PrivateBucketAccess": is_private
    }
    
    if endpoint is not None:
        body["Endpoint"] = endpoint
    if region is not None:
        body["Region"] = region
        
    if is_private and task_type == 's3' and ak and sk:
        body["AuthInformation"] = {
            "AccessKeyID": ak,
            "AccessKeySecret": sk
        }
    
    try:
        if hasattr(client, 'create_offline_log_store_task'):
            res = client.create_offline_log_store_task(body)
        else:
            # SDK 缺失预定义 API，动态注册补充
            from byteplus_sdk.cdn.service import ApiInfo
            client.api_info['CreateOfflineLogStoreTask'] = ApiInfo(
                "POST", "/", {"Action": "CreateOfflineLogStoreTask", "Version": "2021-03-01"}, {}, {"Content-Type": "application/json"}
            )
            res = client.json('CreateOfflineLogStoreTask', {}, body)
            if isinstance(res, bytes):
                res = json.loads(res.decode('utf-8'))
                
            # 判断响应中是否有业务错误，如果有则抛出异常以便 CLI 显示为 Error
            if isinstance(res, str):
                res_dict = json.loads(res)
            else:
                res_dict = res
            
            if "ResponseMetadata" in res_dict and "Error" in res_dict["ResponseMetadata"]:
                error_info = res_dict["ResponseMetadata"]["Error"]
                raise Exception(f"{error_info.get('Code')}: {error_info.get('Message')}")
                
        click.echo(f"Success: {json.dumps(res, indent=2)}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@log_offline.command('tos')
@common_offline_options
@click.option('--private-bucket', type=click.Choice(['yes', 'no']), default='no', prompt='Is this a private bucket? (yes, no)', help='Private bucket access')
@click.option('--region', type=click.Choice(['HongKong', 'Johor', 'Jakarta']), prompt='Please enter Region', default='HongKong', help='TOS Region')
def log_offline_tos(bucket, domain, private_bucket, region):
    """Create offline log task for TOS"""
    is_private = private_bucket == 'yes'
    
    region_map = {
        'HongKong': 'cn-hongkong',
        'Johor': 'ap-southeast-1',
        'Jakarta': 'ap-southeast-3'
    }
    pure_region = region_map.get(region, 'cn-hongkong')
    
    endpoint_map = {
        'cn-hongkong': 'tos-cn-hongkong.bytepluses.com',
        'ap-southeast-1': 'tos-ap-southeast-1.bytepluses.com',
        'ap-southeast-3': 'tos-ap-southeast-3.bytepluses.com'
    }
    endpoint = endpoint_map.get(pure_region, 'tos-ap-southeast-3.bytepluses.com')
    
    handle_log_offline(bucket, domain, endpoint, pure_region, 'tos', is_private=is_private)

@log_offline.command('s3')
@common_offline_options
@click.option('--endpoint', required=True, prompt='Please enter storage Endpoint', help='Storage endpoint')
@click.option('--region', required=True, prompt='Please enter Region', help='Storage region')
@click.option('--private-bucket', type=click.Choice(['yes', 'no']), default='no', prompt='Is this a private bucket? (yes, no)', help='Private bucket access')
@click.option('--ak', help='AccessKey ID for s3 private bucket')
@click.option('--sk', help='AccessKey Secret for s3 private bucket')
def log_offline_s3(bucket, domain, endpoint, region, private_bucket, ak, sk):
    """Create offline log task for S3"""
    is_private = private_bucket == 'yes'
    if is_private:
        if not ak:
            ak = click.prompt('Please enter AccessKey ID', default='')
        if not sk:
            sk = click.prompt('Please enter AccessKey Secret', hide_input=True, default='')
    
    # Check if endpoint needs https:// prefix
    if not endpoint.startswith('http://') and not endpoint.startswith('https://'):
        endpoint = 'https://' + endpoint
        
    handle_log_offline(bucket, domain, endpoint, region, 's3', is_private=is_private, ak=ak, sk=sk)

@cli.group()
def log_realtime():
    """Create a realtime log delivery task."""
    pass

def common_realtime_options(f):
    f = click.option('--domain', required=True, prompt='Please enter associated domains (comma separated, or use "all" for all domains)', help='Associated domains')(f)
    f = click.option('--desc', help='Task description')(f)
    f = click.option('--sample-rate', type=float, default=100.0, help='Sample rate (0.00-100.00)')(f)
    return f

def handle_log_realtime(domain, task_type, desc, sample_rate, target_config_dict):
    if domain.lower() == 'all':
        domain = '*'
        
    client = init_cdn_client()
    body = {
        "Area": "outside_chinese_mainland",
        "Domain": domain,
        "TaskType": task_type
    }
    if desc:
        body["Desc"] = desc
    if sample_rate is not None:
        body["SampleRate"] = sample_rate
        
    body.update(target_config_dict)

    try:
        if hasattr(client, 'create_realtime_log_delivery_task'):
            res = client.create_realtime_log_delivery_task(body)
        else:
            # SDK 没有提供预定义的方法时，我们需要手动补充缺失的 API 信息
            # 这是解决 "no such api" 和签名错误的必要配置
            from byteplus_sdk.cdn.service import ApiInfo
            client.api_info['CreateRealtimeLogDeliveryTask'] = ApiInfo(
                "POST", "/", {"Action": "CreateRealtimeLogDeliveryTask", "Version": "2021-03-01"}, {}, {"Content-Type": "application/json"}
            )
            res = client.json('CreateRealtimeLogDeliveryTask', {}, body)
            if isinstance(res, bytes):
                res = json.loads(res.decode('utf-8'))
            
            # 判断响应中是否有业务错误，如果有则抛出异常以便 CLI 显示为 Error
            if isinstance(res, str):
                res_dict = json.loads(res)
            else:
                res_dict = res
            
            if "ResponseMetadata" in res_dict and "Error" in res_dict["ResponseMetadata"]:
                error_info = res_dict["ResponseMetadata"]["Error"]
                raise Exception(f"{error_info.get('Code')}: {error_info.get('Message')}")
                
        click.echo(f"Success: {json.dumps(res, indent=2)}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@log_realtime.command('tls')
@common_realtime_options
@click.option('--project-id', required=True, prompt='Please enter TLS Project ID', help='TLS Project ID')
@click.option('--region', type=click.Choice(['HongKong', 'Johor', 'Jakarta']), prompt='Please enter Region', default='HongKong', help='TLS Region')
@click.option('--topic-name', required=True, prompt='Please enter TLS Topic Name', help='TLS Topic Name')
@click.option('--ttl', type=int, required=True, prompt='Please enter TLS TTL in days (1-3650)', default=30, help='TLS TTL in days (1-3650)')
def log_realtime_tls(domain, desc, sample_rate, project_id, region, topic_name, ttl):
    """Deliver realtime logs to TLS"""
    # 映射城市名到 Region ID
    region_map = {
        'HongKong': 'cn-hongkong',
        'Johor': 'ap-southeast-1',
        'Jakarta': 'ap-southeast-3'
    }
    pure_region = region_map.get(region, 'cn-hongkong')
    
    # 自动根据 Region 注入 TLS Endpoint
    endpoint_map = {
        'cn-hongkong': 'https://tls-cn-hongkong.bytepluses.com',
        'ap-southeast-1': 'https://tls-ap-southeast-1.bytepluses.com',
        'ap-southeast-3': 'https://tls-ap-southeast-3.bytepluses.com'
    }
    tls_endpoint = endpoint_map.get(pure_region, 'https://tls-ap-southeast-3.bytepluses.com')

    tls_config = {
        "Endpoint": tls_endpoint,
        "ProjectID": project_id,
        "TopicName": topic_name
    }
    if ttl is not None:
        tls_config["Ttl"] = ttl
    handle_log_realtime(domain, 'tls', desc, sample_rate, {"Tls": tls_config})

@log_realtime.command('sls')
@common_realtime_options
@click.option('--ak', required=True, prompt='Please enter Aliyun AccessKey ID', help='Aliyun AccessKey ID')
@click.option('--sk', required=True, prompt='Please enter Aliyun AccessKey Secret', hide_input=True, help='Aliyun AccessKey Secret')
@click.option('--sls-endpoint', required=True, prompt='Please enter SLS Endpoint', help='SLS Endpoint')
@click.option('--log-store', required=True, prompt='Please enter SLS LogStore', help='SLS LogStore')
@click.option('--project', required=True, prompt='Please enter SLS Project', help='SLS Project')
def log_realtime_sls(domain, desc, sample_rate, ak, sk, sls_endpoint, log_store, project):
    """Deliver realtime logs to SLS"""
    sls_config = {
        "AccessKeyId": ak,
        "AccessKeySecret": sk,
        "Endpoint": sls_endpoint,
        "LogStore": log_store,
        "Project": project
    }
    handle_log_realtime(domain, 'sls', desc, sample_rate, {"Sls": sls_config})

@log_realtime.command('http_server')
@common_realtime_options
@click.option('--url', required=True, prompt='Please enter HTTP Server URL', help='HTTP Server URL')
@click.option('--auth-mechanism', type=bool, prompt='Enable AuthMechanism? (True/False)', default=False, help='Enable authentication')
@click.option('--secret-key', help='Auth Secret Key')
@click.option('--compress-type', type=click.Choice(['gzip']), help='Compress type')
def log_realtime_http(domain, desc, sample_rate, url, auth_mechanism, secret_key, compress_type):
    """Deliver realtime logs to HTTP Server"""
    if auth_mechanism and not secret_key:
        secret_key = click.prompt('Please enter Auth Secret Key', hide_input=True)
        
    http_config = {
        "Url": url,
        "AuthMechanism": auth_mechanism
    }
    if auth_mechanism and secret_key:
        http_config["SecretKey"] = secret_key
    if compress_type:
        http_config["CompressType"] = compress_type
    handle_log_realtime(domain, 'http_server', desc, sample_rate, {"HttpServer": http_config})

@log_realtime.command('splunk')
@common_realtime_options
@click.option('--url', required=True, prompt='Please enter Splunk HEC URL', help='Splunk HEC URL')
@click.option('--token', required=True, prompt='Please enter Splunk HEC Token', hide_input=True, help='Splunk HEC Token')
@click.option('--compress-type', type=click.Choice(['gzip']), help='Compress type')
def log_realtime_splunk(domain, desc, sample_rate, url, token, compress_type):
    """Deliver realtime logs to Splunk"""
    splunk_config = {
        "Url": url,
        "Token": token
    }
    if compress_type:
        splunk_config["CompressType"] = compress_type
    handle_log_realtime(domain, 'splunk', desc, sample_rate, {"Splunk": splunk_config})

@log_realtime.command('bigquery')
@common_realtime_options
@click.option('--project-id', required=True, prompt='Please enter GCP Project ID', help='GCP Project ID')
@click.option('--dataset-id', required=True, prompt='Please enter BigQuery Dataset ID', help='BigQuery Dataset ID')
@click.option('--table-id', required=True, prompt='Please enter BigQuery Table ID', help='BigQuery Table ID')
@click.option('--auth-str', help='GCP Auth JSON string (must be single-line serialized JSON)')
@click.option('--auth-file', help='Path to GCP Auth JSON file (mutually exclusive with --auth-str)')
def log_realtime_bigquery(domain, desc, sample_rate, project_id, dataset_id, table_id, auth_str, auth_file):
    """Deliver realtime logs to BigQuery"""
    if not auth_str and not auth_file:
        auth_str = click.prompt('Please provide Google Cloud Auth JSON string', hide_input=True)
    
    if auth_file:
        import os
        if not os.path.exists(auth_file):
            click.echo(f"Error: File not found - {auth_file}", err=True)
            return
        with open(auth_file, 'r', encoding='utf-8') as f:
            try:
                parsed = json.load(f)
                # Google BigQuery requires exactly single-line string with escaped newlines and quotes
                # The prompt example shows it needs to be serialized into a JSON string inside the JSON payload
                auth_str = json.dumps(parsed)
            except Exception as e:
                click.echo(f"Error parsing JSON file: {e}", err=True)
                return

    bq_config = {
        "ProjectID": project_id,
        "DatasetID": dataset_id,
        "TableID": table_id,
        "Authentication": auth_str
    }
    handle_log_realtime(domain, 'bigquery', desc, sample_rate, {"BigQuery": bq_config})


if __name__ == '__main__':
    cli()
