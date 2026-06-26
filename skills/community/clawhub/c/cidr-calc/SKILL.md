---
name: cidr-calc
description: Calculate subnet information from CIDR notation. Use when the user asks to calculate a subnet, find the network address, broadcast address, host range, subnet mask, or number of hosts for an IP in CIDR notation like 192.168.1.0/24.
---

# CIDR Calculator

Given an IP address in CIDR notation, compute all subnet parameters: network address, broadcast, host range, subnet mask, wildcard mask, host counts, IP class, and binary representation.

## Input
- A CIDR notation string in the format `A.B.C.D/N` (e.g. `192.168.1.0/24`)

## Output
A structured result with these fields:
- CIDR Notation (normalized)
- Network Address
- Broadcast Address
- Subnet Mask
- Wildcard Mask
- First Usable Host
- Last Usable Host
- Total Hosts (2^(32-N))
- Usable Hosts
- IP Class (A / B / C / D Multicast / E Reserved)
- Network Type (Private / Public)
- Binary Representation of the IP

## Instructions
1. Validate the input. It must match `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}`. Each octet must be 0–255. Prefix must be 0–32.
2. Compute values using standard subnet math:
   - `maskNum = (0xFFFFFFFF << (32 - prefix)) >>> 0`
   - `wildcardNum = ~maskNum >>> 0`
   - `networkNum = (ipNum & maskNum) >>> 0`
   - `broadcastNum = (networkNum | wildcardNum) >>> 0`
   - `totalHosts = 2^(32 - prefix)`
   - `usableHosts`: if prefix == 32 → 1; if prefix == 31 → 2; else `totalHosts - 2`
3. Determine IP class from first octet:
   - 1–126 → A; 128–191 → B; 192–223 → C; 224–239 → D (Multicast); 240–255 → E (Reserved); 127 → Loopback
4. Determine private vs public:
   - Private: 10.x.x.x, 172.16–31.x.x, 192.168.x.x, 127.x.x.x (loopback)
5. Compute binary as four 8-bit groups joined by dots.
6. Present results in a clear labeled format.

### Quick CIDR reference
| CIDR | Subnet Mask       | Total Hosts |
|------|-------------------|-------------|
| /8   | 255.0.0.0         | 16,777,216  |
| /16  | 255.255.0.0       | 65,536      |
| /20  | 255.255.240.0     | 4,096       |
| /22  | 255.255.252.0     | 1,024       |
| /24  | 255.255.255.0     | 256         |
| /28  | 255.255.255.240   | 16          |
| /30  | 255.255.255.252   | 4           |
| /32  | 255.255.255.255   | 1           |

## Options
- Input is always a single CIDR string; no additional options.

## Examples

**Input:** `192.168.1.0/24`

**Output:**
```
CIDR Notation:   192.168.1.0/24
Network Address: 192.168.1.0
Broadcast:       192.168.1.255
Subnet Mask:     255.255.255.0
Wildcard Mask:   0.0.0.255
First Host:      192.168.1.1
Last Host:       192.168.1.254
Total Hosts:     256
Usable Hosts:    254
IP Class:        C
Network Type:    Private
Binary:          11000000.10101000.00000001.00000000
```

**Input:** `10.0.0.0/8`

**Output:**
```
CIDR Notation:   10.0.0.0/8
Network Address: 10.0.0.0
Broadcast:       10.255.255.255
Subnet Mask:     255.0.0.0
Wildcard Mask:   0.255.255.255
First Host:      10.0.0.1
Last Host:       10.255.255.254
Total Hosts:     16,777,216
Usable Hosts:    16,777,214
IP Class:        A
Network Type:    Private
Binary:          00001010.00000000.00000000.00000000
```

## Error Handling
- If the input is not valid CIDR notation, say so and provide the expected format (`A.B.C.D/N`).
- If an octet exceeds 255 or the prefix exceeds 32, explain the validation error.
- If the user provides an IP without a prefix (e.g. `192.168.1.1`), ask for the prefix length or assume /32.
