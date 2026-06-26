# Changelog

## [1.2.0] - 2026-03-13

### Added - Agent Usability Improvements

**Priority improvements based on agent feedback:**

1. **Clear dependency documentation**
   - New `DEPENDENCIES.md` - Explicit install instructions
   - Dependency matrix showing what each script needs
   - README updated with upfront dependency section

2. **Minimal bare-subdomain script**
   - New `create-subdomain.js` - Create subdomains WITHOUT IPFS
   - Fewer dependencies (only viem, no content-hash)
   - Faster execution for basic subdomain workflows

3. **Multiple wallet input methods**
   - All scripts now support: --keystore + --password
   - New: --private-key-env (read from environment variable)
   - New: --private-key (direct input, less secure)
   - Flexible authentication for different agent setups

4. **Quick operational examples**
   - New `QUICK-START.md` - Copy-paste commands for agents
   - Decision trees for choosing the right script
   - State verification patterns
   - Resumability guidance for interrupted workflows

5. **Documentation reorganization**
   - Core vs Extended features clearly separated
   - Dependency requirements specified per-script
   - Performance tips and debugging guidance

### Changed

- Version bumped to 1.2.0
- README: Added dependency section upfront
- SKILL.md: Updated requirements to show optional vs required

### Technical Details

**New files:**
- `scripts/create-subdomain.js` - Minimal subdomain creation
- `DEPENDENCIES.md` - Comprehensive dependency guide
- `QUICK-START.md` - Operational reference for agents
- `CHANGELOG.md` - This file

**Updated files:**
- `README.md` - Dependency section added, structure improved
- `SKILL.md` - Version 1.2.0, updated requirements
- `VERSION` - 1.2.0

**Dependency matrix:**
| Script | viem | content-hash |
|--------|------|--------------|
| check-ens-name.js | Required | Optional |
| register-ens-name.js | Required | Not used |
| create-subdomain.js | Required | Not used |
| create-subdomain-ipfs.js | Required | Required |

---

## [1.1.0] - 2026-03-12

### Added

- Three-phase ENS registration script
- Accurate cost documentation
- ENS pricing tiers (3/4/5+ character names)
- Contract addresses documented
- Troubleshooting guide

### Changed

- Initial public release

---

## Feedback Welcome

This version addresses agent usability feedback. Additional improvements welcome!

**Key improvements requested:**
- ✅ Clear dependency/install section
- ✅ Minimal create-subdomain script
- ✅ Multiple wallet input methods
- ✅ Quick operational examples
- ✅ Resumability guidance

**Future possibilities:**
- Batch operations
- Testnet support
- Transaction retry logic
- More resolver configurations
