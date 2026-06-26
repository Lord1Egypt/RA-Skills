import os
from byteplus_sdk.cdn.service import CDNService

def init_cdn_client():
    # 只从项目根目录加载 .env 文件（安全边界）
    # 项目根目录是 scripts 目录的父级
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(scripts_dir)
    env_path = os.path.join(project_root, '.env')
    
    if env_path and os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    key = k.strip()
                    # 只加载与 BytePlus CDN 相关的环境变量，限制权限边界
                    if key in ['BYTEPLUS_AK', 'BYTEPLUS_SK']:
                        os.environ.setdefault(key, v.strip().strip("'").strip('"'))

    # byteplus-sdk-python 默认 region 是 ap-singapore-1
    cdn_service = CDNService('ap-singapore-1')
    ak = os.environ.get('BYTEPLUS_AK')
    sk = os.environ.get('BYTEPLUS_SK')
    
    if not ak or not sk:
        import click
        click.echo("Environment variables BYTEPLUS_AK and BYTEPLUS_SK are not set. Asking for input...")
        if not ak:
            ak = click.prompt('Please enter BYTEPLUS_AK', type=str)
        if not sk:
            sk = click.prompt('Please enter BYTEPLUS_SK', type=str, hide_input=True)
            
    # 去除可能存在的首尾空格
    ak = ak.strip() if ak else ak
    sk = sk.strip() if sk else sk
    
    cdn_service.set_ak(ak)
    cdn_service.set_sk(sk)
    
    import click
    return cdn_service
