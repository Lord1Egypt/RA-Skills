"""Boto3 client factory for AWS EMR services.

Exports:
    get_emr_serverless_client: Client for EMR Serverless.
    get_emr_client: Client for EMR on EC2.
    get_emr_containers_client: Client for EMR on EKS.
    get_s3_client: Client for Amazon S3.
"""

from scripts.client.boto_client import (
    get_emr_client,
    get_emr_containers_client,
    get_emr_serverless_client,
    get_s3_client,
)

__all__ = [
    "get_emr_serverless_client",
    "get_emr_client",
    "get_emr_containers_client",
    "get_s3_client",
]
