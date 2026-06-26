# Vast.ai Port Mapping Reference

## Critical Concept

Vast.ai uses **Caddy reverse proxy** to route external ports to container internal ports.

Environment variables: `VAST_TCP_PORT_<INTERNAL>=<EXTERNAL>`

Example from our deployment:
```
VAST_TCP_PORT_22=26661      # SSH
VAST_TCP_PORT_8384=26565    # Maps to upscaler (we use internal 19000)
VAST_TCP_PORT_1111=26833    # Maps to compressor (we use internal 19001)
```

## Occupied Ports (DO NOT USE)

| Internal | External | Service | Owner |
|----------|----------|---------|-------|
| 8080 | 26812 | Jupyter Notebook | Vast.ai default |
| 11111 | 26995 | Instance Portal | Vast.ai |
| 18384 | varies | Syncthing | Vast.ai |

## Our Miner Mapping

| Service | Internal Listen | Caddy Route | External Port | Axon Advertised |
|---------|----------------|-------------|---------------|-----------------|
| Upscaler Backend | 19000 | :8384 → 19000 | 26565 | 26565 |
| Compressor Backend | 19001 | :1111 → 19001 | 26833 | 26833 |

## Verification

```bash
# 1. Check miners are bound
netstat -tuln | grep -E ':19000|:19001'

# 2. Check Caddy routing
curl localhost:8384  # Should hit upscaler
curl localhost:1111  # Should hit compressor

# 3. Check external access (from outside)
curl http://<VAST_IP>:26565  # Should return axon 404, NOT 401
curl http://<VAST_IP>:26833
```

## Common Mistake

❌ Using `--axon.port 8384` because that's what Caddy listens on  
✅ Use `--axon.port 19000 --axon.external_port 26565`

The miner listens on 19000 (internal), Caddy forwards :8384 → :19000, validators connect to external 26565.
