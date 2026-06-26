# ClawHub Preflight Checklist for CPA Manager

## ✅ Pre-Upload Verification

This document serves as a final checklist before uploading the CPA Manager skill to ClawHub.

### 1. Sensitive Data Removal Verification

**✅ Configuration Files**
- [x] Real tokens removed from all configuration files
- [x] `config.json` replaced with `config.example.json`
- [x] Example configuration uses placeholder values only
- [x] No hardcoded credentials in any script files

**✅ Documentation Review**
- [x] All documentation uses generic paths (`/path/to/cpa-manager`)
- [x] No specific server URLs, IP addresses, or hostnames exposed
- [x] Token examples use placeholder values (`your-management-token`)
- [x] No internal company-specific references remain

**✅ Code Audit**
- [x] Scripts don't contain hardcoded sensitive data
- [x] Environment variable names are generic
- [x] No debug output that could leak sensitive information
- [x] All file paths in code are relative or configurable

### 2. File Inclusion Verification

**✅ Included Files (Distribution Ready)**
- [x] `SKILL.md` - Updated, generic documentation
- [x] `_meta.json` - Skill metadata
- [x] `scripts/` directory with essential Python scripts only
- [x] `references/` directory with workflow documentation
- [x] `config.example.json` - Safe configuration template
- [x] `safety.md` - Safety guidelines
- [x] `troubleshooting.md` - Troubleshooting guide
- [x] `clawhub-preflight.md` - This checklist

**✅ Excluded Files (Correctly Omitted)**
- [x] `config.json` - Real configuration (excluded)
- [x] `*.log` files - Log files (excluded)
- [x] `*.sqlite3` files - Database files (excluded)
- [x] `*_accounts.json` - Account export files (excluded)
- [x] `backup-*` directories - Backup directories (excluded)
- [x] `__pycache__` directories - Python cache (excluded)
- [x] Any temporary or working files (excluded)

### 3. Functionality Verification

**✅ Core Scripts Present**
- [x] `cpa_warden.py` - Main CPA warden script
- [x] `scan_cpa.py.bak` - Scan script (backup version)
- [x] `delete_401_only.py` - Targeted 401 deletion script
- [x] `reenable_quota.py` - Quota account recovery script
- [x] `clean_codex_accounts.py` - Account cleanup utility

**✅ Documentation Completeness**
- [x] Installation and setup instructions
- [x] Usage examples with safe parameters
- [x] Safety guidelines and warnings
- [x] Troubleshooting procedures
- [x] Best practices and recommendations

### 4. License and Attribution

**✅ Open Source Compliance**
- [x] Based on official cpa-warden (https://github.com/fantasticjoe/cpa-warden)
- [x] Proper attribution to original project
- [x] Compatible license terms
- [x] No proprietary code included without permission

### 5. ClawHub Specific Requirements

**✅ Metadata Validation**
- [x] `_meta.json` contains valid skill name and description
- [x] Skill name matches directory name (`cpa-manager`)
- [x] Description is clear and accurate
- [x] No reserved characters or invalid formatting

**✅ Directory Structure**
- [x] Follows ClawHub skill directory conventions
- [x] Clean, flat structure without unnecessary nesting
- [x] All required files in correct locations
- [x] No hidden files or system artifacts

## 📋 Final Upload Instructions

### Before Uploading
1. **Double-check** this preflight checklist
2. **Verify** no sensitive data remains in any file
3. **Test** the skill package locally if possible
4. **Review** all documentation for clarity and accuracy

### Upload Process
1. Navigate to ClawHub web interface
2. Select "Upload New Skill" 
3. Choose the skill package directory
4. Review the file list before confirming upload
5. Add appropriate tags: `cpa`, `cli-proxy-api`, `account-management`, `maintenance`

### Post-Upload Verification
1. Install the skill from ClawHub in a test environment
2. Verify all files are present and accessible
3. Test basic functionality with safe parameters
4. Confirm documentation renders correctly
5. Validate that example configuration works as expected

## ⚠️ Critical Reminders

- **Never** upload skills containing real credentials or sensitive configuration
- **Always** test uploaded skills in isolated environments first
- **Regularly** update skills to incorporate security fixes and improvements
- **Monitor** skill usage and provide support documentation

## 📞 Support Contact

For issues with this ClawHub skill package:
- Report issues on the original cpa-warden GitHub repository
- Contact your CPA deployment administrator for environment-specific issues
- Reach out to ClawHub support for platform-related problems

---
*Last updated: $(date)*
*Package version: 1.0.0*
*Based on cpa-warden upstream version: [specify version if known]*