"""
manage_instance.py - Manage database instance

Register new database instance to DBDoctor platform.
"""

import argparse
import base64
import json
import sys

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from common import client
from common.config import config


class RSAUtils:
    """RSA encryption utility class (used to encrypt database password during management)"""
    
    PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuvJKNhSl6pmfNYqLLADJ1M59E3TW4ldYcq0PGpMlDLiNbjHW1Jt14zuNPxc+x2HFUPTHgngSHhURD0ZXJjYCkLmkOKVxv/9nZS3Thp5oJNXjk6wZEqneaaNdYT4KgSVc7DhO3oXXUFyrNzNNffs5paQ1Zd2JZhDYZxgpMlh2FMixkIz8znX8HDvLP8Fg5ImzoA50ljoV6w52EBRdo9+YO3zsflMFdLJnj10SDJyFcmI6rhXoE/C3eFMVyNdoPYQFVgHkyl6HTE92OVzSB41u/F9kQaawBll5KsgUs6XwmSK9NWVBz6i5M/vgP9A2Yz6aS+ZeenDm2gjjOiwETSqRsQIDAQAB
-----END PUBLIC KEY-----"""

    @staticmethod
    def encrypt_password(password: str) -> str:
        """
        RSA public key encryption for password
        :param password: Plaintext password
        :return: Base64 encoded encrypted result
        """
        key = RSA.import_key(RSAUtils.PUBLIC_KEY.strip())
        cipher = PKCS1_v1_5.new(key)
        
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        encrypted_data = cipher.encrypt(password)
        return base64.b64encode(encrypted_data).decode('utf-8')


def check_db_connectivity(
    ip: str,
    port: int,
    engine: str,
    db_user: str,
    encrypted_password: str,
) -> dict:
    """
    Check database connectivity.

    Args:
        ip: Database server IP
        port: Database port
        engine: Database engine
        db_user: Database username
        encrypted_password: RSA encrypted password
    Returns:
        API JSON response, including dbVersion and other info
    """
    params = {
        "Ip": ip,
        "Port": port,
        "Engine": engine,
        "UserAccount": db_user,
        "UserPassword": encrypted_password,
        "Role": config.role,
        "UserId": config.user_id,
    }
    return client.get("/drapi/CheckDBUserPrivilege", params=params)


def manage_instance(
    ip: str,
    port: int,
    engine: str,
    db_user: str,
    db_password: str,
    tenant: str,
    project: str,
    description: str = "",
) -> dict:
    """
    Manage database instance.
    Process: 1. Check connectivity 2. Get database version 3. Execute management

    Args:
        ip: Database server IP
        port: Database port
        engine: Database engine (mysql/oracle/postgresql/dm/sqlserver/oracle-rac)
        db_user: Database username
        db_password: Database password (plaintext)
        tenant: Tenant name
        project: Project name
        description: Instance description (optional)
    Returns:
        API JSON response
    """
    # 1. RSA encrypt password
    encrypted_password = RSAUtils.encrypt_password(db_password)

    # 2. Check database connectivity
    check_result = check_db_connectivity(ip, port, engine, db_user, encrypted_password)
    if not check_result.get("Success"):
        error_msg = check_result.get("Message", "Connectivity check failed")
        raise Exception(f"Database connectivity check failed: {error_msg}")

    # 3. Get database version
    db_version = check_result.get("Data", {}).get("dbVersion")
    if not db_version:
        raise Exception("Unable to get database version")

    # 4. Build management request body
    json_body = {
        "engine": engine,
        "ip_port": f"{ip}:{port}",
        "cpu": 1,
        "dbUser": db_user,
        "dbPwd": encrypted_password,
        "dbVersion": db_version,
        "nodePort": 22,
        "collectDatabase": "",
        "resourceQueryType": 6,
        "otherConnInfo": "",
        "retainTime": 3,
        "deployType": 1,
        "autoDeployPath": "/root/dbdoctor",
        "thirdPartyInfo": "{}",
        "auditRetainDays": 1,
        "lockAnalysisOn": 0,
        "managed": 1,
        "diskType": 1,
        "dockOggManage": {"state": False},
        "db2IndexRecommend": {},
        "ip": ip,
        "port": port,
        "tenantName": tenant,
        "projectName": project,
        "role": "",
        "parentId": "",
        "deployMode": "",
        "nodeSyncManaged": 1,
        "clusterMode": None,
        "dataSyncCollectManaged": 0,
        "userRole": config.role,
        "userId": config.user_id,
    }
    if description:
        json_body["description"] = description

    # 5. Execute management
    return client.post(
        "/drapi/instanceCreate",
        params={
            "Role": config.role,
            "Tenant": tenant,
            "Action": "instanceCreate",
            "Project": project,
            "UserId": config.user_id,
        },
        json_body=json_body,
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Register new database instance to DBDoctor platform")
    parser.add_argument("--ip", required=True, help="Database server IP")
    parser.add_argument("--port", required=True, type=int, help="Database port")
    parser.add_argument("--engine", required=True,
                        choices=["mysql", "oracle", "postgresql", "dm", "sqlserver", "oracle-rac"],
                        help="Database engine")
    parser.add_argument("--db-user", required=True, help="Database username")
    parser.add_argument("--db-password", required=True, help="Database password (plaintext, auto RSA encrypted by program)")
    # db_version is now automatically obtained through connectivity check, no longer needs user input
    parser.add_argument("--tenant", required=True, help="Tenant name")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--description", default="", help="Instance description (optional)")
    args = parser.parse_args()

    try:
        result = manage_instance(
            ip=args.ip,
            port=args.port,
            engine=args.engine,
            db_user=args.db_user,
            db_password=args.db_password,
            tenant=args.tenant,
            project=args.project,
            description=args.description,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
