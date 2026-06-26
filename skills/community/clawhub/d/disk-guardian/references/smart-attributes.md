# SMART Attributes Reference

Plain-English guide to the 10 most critical SMART attributes and what they mean for drive health.

---

## 1. Reallocated Sector Count (ID 5)

**What it is:** The number of bad sectors the drive has found and moved ("reallocated") to a spare area.

**What it means:** Any non-zero value is a red flag. The drive found physical damage and worked around it. A value of 1–5 means the drive is still working but degrading. Higher values mean faster degradation. The drive will eventually run out of spare sectors and fail. **Back up immediately and plan to replace.**

---

## 2. Current Pending Sector Count (ID 197)

**What it is:** Sectors that failed to read successfully and are queued for reallocation — but haven't been remapped yet.

**What it means:** These sectors might recover (if a future write succeeds) or become permanently bad. Any non-zero count means data in those sectors may already be lost. This is a **pre-failure indicator** — treat it like a "check engine" light that's about to turn into smoke.

---

## 3. Uncorrectable Sector Count (ID 198)

**What it is:** Sectors that couldn't be read during an offline scan even with error correction.

**What it means:** These sectors are genuinely unreadable. Data in them is gone. Even one uncorrectable error is serious. The drive has regions that cannot be trusted. **Back up everything and replace.**

---

## 4. Reported Uncorrectable Errors (ID 187)

**What it is:** Read/write errors that the drive's ECC (error correction) could not fix during normal operation.

**What it means:** Unlike attribute 198 (which is offline scans), these errors happened during real use — meaning real files may have been silently corrupted. Any non-zero value warrants immediate action.

---

## 5. Power-On Hours (ID 9)

**What it is:** Total number of hours the drive has been powered on over its lifetime.

**What it means:** Not a health indicator by itself, but provides context. Most HDDs are rated for 30,000–50,000 hours. SSDs vary more widely. Over 40,000 hours: plan for replacement. Over 60,000 hours: the drive is living on borrowed time regardless of other indicators.

---

## 6. Temperature (ID 190 / 194)

**What it is:** Current drive temperature in Celsius.

**Thresholds:**
- Under 45°C: Normal
- 45–50°C: Warm but acceptable
- 50–60°C: Warning — check airflow
- Over 60°C: Critical — risk of damage and data loss

**What it means:** Heat accelerates all forms of drive failure. A consistently hot drive has a shorter lifespan. Check case airflow, fan health, and drive placement if temps are elevated.

---

## 7. Read Error Rate (ID 1)

**What it is:** Raw count of hardware read errors.

**What it means:** On most drives (especially Seagate), the raw value is very high by design — it includes corrected errors, so you can ignore the raw number. What matters is the **normalized value**: if it drops below the threshold (usually 51), the drive is failing. Focus on the normalized value, not raw.

---

## 8. Command Timeout (ID 188)

**What it is:** Number of times a command timed out before the drive could respond.

**What it means:** Usually a sign of a struggling drive, but can also indicate a bad SATA cable or loose connector. If you see this alongside other errors, it's likely the drive. If it's isolated, try replacing the cable first.

---

## 9. End-to-End Error (ID 184)

**What it is:** Counts mismatches between data in the drive's RAM buffer and what was actually written to disk.

**What it means:** The drive's internal data path is corrupted — data was modified between the cache and the platters/flash. This is serious internal hardware corruption. Any non-zero value warrants replacement.

---

## 10. Seek Error Rate (ID 7)

**What it is:** Rate of errors when the drive's head tries to find a track (HDD only).

**What it means:** Similar to Read Error Rate — on most drives the raw value is large by design. Normalized value matters. If the normalized value drops below threshold, the heads are having trouble positioning, which leads to read/write failures. High seek error rates on an older drive indicate mechanical wear.

---

## NVMe-Specific Indicators

NVMe drives don't use the SMART attribute table. They report health via a separate log:

| Field | Warning Threshold | What It Means |
|-------|-------------------|---------------|
| **Available Spare** | ≤ spare threshold (usually 10%) | Percentage of spare blocks left. When exhausted, drive stops writing. |
| **Percentage Used** | > 80% | Estimated endurance consumed. 100% doesn't mean dead, but drive is near end-of-rated-life. |
| **Critical Warning** | Any non-zero | Hardware-level flags: spare space low, temperature warning, degraded reliability, media in read-only mode. |
| **Media and Data Integrity Errors** | Any non-zero | Internal media errors that couldn't be corrected. Indicates hardware failure. |
| **Unsafe Shutdowns** | > 100 (context-dependent) | Times the drive wasn't cleanly shut down. High on laptops; concerning only if very high (thousands). |

---

## Quick Reference: What Needs Immediate Action

| Indicator | Action |
|-----------|--------|
| Reallocated Sector Ct > 0 | Back up now, replace soon |
| Current Pending Sector > 0 | Back up immediately |
| Uncorrectable Errors > 0 | Back up immediately, replace |
| NVMe Media Errors > 0 | Replace drive |
| NVMe Critical Warning ≠ 0 | Investigate immediately |
| Temperature > 60°C | Fix cooling or replace |
| SMART Overall Health: FAILED | Emergency backup and replace |
