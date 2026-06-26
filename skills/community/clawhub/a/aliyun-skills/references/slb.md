# SLB / CLB (Server Load Balancer / Classic Load Balancer) Reference

SLB (also called CLB) distributes traffic across backend ECS instances.
For Layer-7 HTTP/HTTPS with advanced routing, see ALB (Application Load Balancer, product code `alb`).

## List Load Balancers

```bash
aliyun slb DescribeLoadBalancers --RegionId cn-hangzhou
```

```bash
aliyun slb DescribeLoadBalancers --RegionId cn-hangzhou \
  --output 'cols=LoadBalancerId,LoadBalancerName,LoadBalancerStatus,Address' \
  'rows=LoadBalancers.LoadBalancer[]'
```

## Get Load Balancer Details

```bash
aliyun slb DescribeLoadBalancerAttribute \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx
```

## Create a Load Balancer

Public-facing (internet):
```bash
aliyun slb CreateLoadBalancer \
  --RegionId cn-hangzhou \
  --LoadBalancerName my-slb \
  --AddressType internet \
  --InternetChargeType paybytraffic \
  --Bandwidth 100
```

Internal (VPC):
```bash
aliyun slb CreateLoadBalancer \
  --RegionId cn-hangzhou \
  --LoadBalancerName my-internal-slb \
  --AddressType intranet \
  --VpcId vpc-xxxxxx \
  --VSwitchId vsw-xxxxxx
```

## Delete a Load Balancer

> ⚠️ All listeners must be deleted or stopped first.

```bash
aliyun slb DeleteLoadBalancer \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx
```

---

## Listeners

### List Listeners

```bash
aliyun slb DescribeLoadBalancerListeners \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx
```

### Create a TCP Listener (Port 80)

```bash
aliyun slb CreateLoadBalancerTCPListener \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx \
  --ListenerPort 80 \
  --BackendServerPort 80 \
  --Bandwidth 100 \
  --HealthCheck on \
  --HealthCheckConnectPort 80
```

### Create an HTTP Listener

```bash
aliyun slb CreateLoadBalancerHTTPListener \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx \
  --ListenerPort 80 \
  --BackendServerPort 80 \
  --Bandwidth 100 \
  --StickySession off \
  --HealthCheck on
```

### Create an HTTPS Listener

```bash
aliyun slb CreateLoadBalancerHTTPSListener \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx \
  --ListenerPort 443 \
  --BackendServerPort 80 \
  --Bandwidth 100 \
  --ServerCertificateId cert-xxxxxx \
  --StickySession off \
  --HealthCheck on
```

### Start / Stop a Listener

```bash
aliyun slb StartLoadBalancerListener \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx \
  --ListenerPort 80

aliyun slb StopLoadBalancerListener \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx \
  --ListenerPort 80
```

### Delete a Listener

```bash
aliyun slb DeleteLoadBalancerListener \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx \
  --ListenerPort 80
```

---

## Backend Servers

### List Backend Servers

```bash
aliyun slb DescribeHealthStatus \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx \
  --ListenerPort 80
```

### Add Backend Servers

```bash
aliyun slb AddBackendServers \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx \
  --BackendServers '[{"ServerId":"i-xxxxxx","Weight":100},{"ServerId":"i-yyyyyy","Weight":100}]'
```

### Remove Backend Servers

```bash
aliyun slb RemoveBackendServers \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx \
  --BackendServers '[{"ServerId":"i-xxxxxx"}]'
```

### Set Backend Server Weight

```bash
aliyun slb SetBackendServers \
  --RegionId cn-hangzhou \
  --LoadBalancerId lb-xxxxxx \
  --BackendServers '[{"ServerId":"i-xxxxxx","Weight":50}]'
```

---

## Server Certificates

### List Certificates

```bash
aliyun slb DescribeServerCertificates --RegionId cn-hangzhou
```

### Upload a Certificate

```bash
aliyun slb UploadServerCertificate \
  --RegionId cn-hangzhou \
  --ServerCertificateName my-cert \
  --ServerCertificate "$(cat /path/to/cert.pem)" \
  --PrivateKey "$(cat /path/to/key.pem)"
```

---

## Load Balancer Status Values

| Status | Meaning |
|--------|---------|
| `active` | Running normally |
| `inactive` | All listeners stopped |
| `locked` | Account locked or overdue |
