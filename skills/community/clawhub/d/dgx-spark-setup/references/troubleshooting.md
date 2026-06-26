# DGX Spark vLLM Troubleshooting

## torch version got downgraded

**Symptom:** vLLM fails to start, CUDA errors, or wrong torch version after any `pip install` or `pip upgrade`.

**Cause:** Regular pip can silently resolve a non-cu130 torch when installing other packages.

**Fix:**
```bash
source ~/vllm-install/.vllm/bin/activate
uv pip install --reinstall torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cu130
# Then reinstall custom Triton:
cd ~/vllm-install/triton
pip install -e python/
```

---

## Triton sm_121 error

**Symptom:** `triton.compiler.errors.CompilationError` or errors mentioning `sm_121` not supported.

**Cause:** Stock Triton doesn't support the GB10 Blackwell architecture.

**Fix:** Rebuild Triton from the pinned commit:
```bash
cd ~/vllm-install/triton
git checkout 4caa0328bf8df64896dd5f6fb9df41b0eb2e750a
pip install -e python/
```

---

## flashinfer import errors or version mismatch

**Symptom:** `ImportError` for flashinfer or cubin errors at startup.

**Fix:** Reinstall both packages together and ensure versions match:
```bash
pip uninstall flashinfer flashinfer-python -y
pip install flashinfer-python
pip install flashinfer
```

---

## nvidia-smi shows N/A for memory

**This is normal.** The DGX Spark uses GB10 unified memory — `nvidia-smi` doesn't report GPU memory the traditional way. The model is loading fine.

---

## vLLM startup hangs at shard loading

**Normal behavior.** Loading 17 safetensor shards for the 120B NVFP4 model takes ~8 minutes on first boot. Watch the log:
```bash
tail -f ~/nemotron.log
```
Wait for: `Application startup complete`

---

## LiteLLM "Unauthorized" from client

**Check:** Is the virtual key in `~/litellm-config.yaml` an exact match to what the client is sending?
```bash
systemctl --user restart litellm
curl -H "Authorization: Bearer sk-your-key" http://localhost:4000/health/liveliness
```

---

## Tailscale blocking SSH / connection refused

**Cause:** ProtonVPN on either the connecting machine or Mac Mini blocks Tailscale traffic (100.x.x.x subnet).

**Fix:** Pause ProtonVPN before connecting, or add split tunneling:
- ProtonVPN → Settings → Split Tunneling → exclude `100.0.0.0/8`

---

## SSH "Too many authentication failures"

**Cause:** SSH agent has too many keys loaded; server cuts off before trying the right one.

**Fix:** Create `~/.ssh/config` on the connecting machine:
```
Host macmini
    HostName <tailscale-ip>
    User jimmy
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```
Then ensure `~/.ssh/authorized_keys` exists on the target machine with your public key.
