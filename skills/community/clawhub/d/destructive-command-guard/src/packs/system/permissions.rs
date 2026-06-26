//! Permissions patterns - protections against dangerous permission changes.
//!
//! This includes patterns for:
//! - chmod 777 (world writable)
//! - chmod -R on system directories
//! - chown -R on system directories
//! - setfacl with dangerous patterns

use crate::packs::{DestructivePattern, Pack, PatternSuggestion, SafePattern};
use crate::{destructive_pattern, safe_pattern};

// ============================================================================
// Suggestion constants (must be 'static for the pattern struct)
// ============================================================================

const CHMOD_777_SUGGESTIONS: &[PatternSuggestion] = &[
    PatternSuggestion::new(
        "chmod 755 {path}",
        "Owner can write; others can read/execute (safer default)",
    ),
    PatternSuggestion::new(
        "chmod u+x {path}",
        "Only add execute for owner instead of world-writable permissions",
    ),
];

const CHOWN_RECURSIVE_SUGGESTIONS: &[PatternSuggestion] = &[
    PatternSuggestion::new(
        "chown {user} {path}",
        "Change ownership of a single path first",
    ),
    PatternSuggestion::new(
        "find {path} -maxdepth 1 -exec chown {user} {} \\;",
        "Limit ownership changes to top-level entries",
    ),
];

/// Create the Permissions pack.
#[must_use]
pub fn create_pack() -> Pack {
    Pack {
        id: "system.permissions".to_string(),
        name: "Permissions",
        description: "Protects against dangerous permission changes like chmod 777, \
                      recursive chmod/chown on system directories",
        keywords: &["chmod", "chown", "chgrp", "setfacl"],
        safe_patterns: create_safe_patterns(),
        destructive_patterns: create_destructive_patterns(),
        keyword_matcher: None,
        safe_regex_set: None,
        safe_regex_set_is_complete: false,
    }
}

fn create_safe_patterns() -> Vec<SafePattern> {
    vec![
        // chmod on files (not directories recursively)
        safe_pattern!(
            "chmod-non-recursive",
            r"chmod\s+(?!-[rR])(?:\d{3,4}|[ugoa][+-][rwxXst]+)\s+[^/]"
        ),
        // stat is safe (read-only)
        safe_pattern!("stat", r"\bstat\b"),
        // ls -l is safe
        safe_pattern!("ls-perms", r"ls\s+.*-[a-zA-Z]*l"),
        // getfacl is safe (read-only)
        safe_pattern!("getfacl", r"\bgetfacl\b"),
        // namei is safe
        safe_pattern!("namei", r"\bnamei\b"),
    ]
}

fn create_destructive_patterns() -> Vec<DestructivePattern> {
    vec![
        // chmod 777 (world writable)
        destructive_pattern!(
            "chmod-777",
            r#"chmod\s+(?:.*\s+)?["'=]?0*777(?:[\s"']|$)"#,
            "chmod 777 makes files world-writable. This is a security risk.",
            High,
            "chmod 777 grants read/write/execute to everyone. This can expose sensitive \
             files and allow unauthorized modification. Prefer least-privilege permissions \
             that only grant the specific access needed.",
            CHMOD_777_SUGGESTIONS
        ),
        // chmod -R on root or system directories
        destructive_pattern!(
            "chmod-recursive-root",
            r"chmod\s+(?:.*(?:-[rR]|--recursive)).*\s+/(?:$|bin|boot|dev|etc|lib|lib64|opt|proc|root|run|sbin|srv|sys|usr|var)\b",
            "chmod -R on system directories can break system permissions.",
            Critical,
            "Recursively changing permissions on system directories can render the system \
             unbootable, break package management, and disrupt every running service. Many \
             system files require specific permission bits to function correctly.\n\n\
             Check current permissions first:\n  \
             ls -la /path/to/directory\n\n\
             Apply changes to a specific subdirectory instead of the whole tree."
        ),
        // chown -R on root or system directories
        destructive_pattern!(
            "chown-recursive-root",
            r"chown\s+(?:.*(?:-[rR]|--recursive)).*\s+/(?:$|bin|boot|dev|etc|lib|lib64|opt|proc|root|run|sbin|srv|sys|usr|var)\b",
            "chown -R on system directories can break system ownership.",
            High,
            "Recursive ownership changes on system directories can disrupt services, \
             break package-managed files, and be difficult to undo. Start with a single \
             path or a shallow find before applying broader changes.",
            CHOWN_RECURSIVE_SUGGESTIONS
        ),
        // chmod u+s (setuid)
        destructive_pattern!(
            "chmod-setuid",
            r"chmod\s+.*u\+s|chmod\s+[4-7]\d{3}",
            "Setting setuid bit (chmod u+s) is a security-sensitive operation.",
            High,
            "The setuid bit causes a program to run with the file owner's privileges \
             regardless of who executes it. If set on the wrong binary, any user can \
             gain elevated access. This is a common privilege escalation vector.\n\n\
             Verify the file and owner first:\n  \
             ls -la <file>\n\n\
             Find existing setuid files:\n  \
             find / -perm -4000 -type f 2>/dev/null"
        ),
        // chmod g+s (setgid)
        destructive_pattern!(
            "chmod-setgid",
            r"chmod\s+.*g\+s|chmod\s+[2367]\d{3}",
            "Setting setgid bit (chmod g+s) is a security-sensitive operation.",
            High,
            "The setgid bit on an executable causes it to run with the file group's \
             privileges. On a directory, new files inherit the directory's group. \
             Misapplication can grant unintended group access to sensitive resources.\n\n\
             Check current group ownership:\n  \
             ls -la <file>\n\n\
             Find existing setgid files:\n  \
             find / -perm -2000 -type f 2>/dev/null"
        ),
        // chown to root
        destructive_pattern!(
            "chown-to-root",
            r"chown\s+.*root[:\s]",
            "Changing ownership to root should be done carefully.",
            High,
            "Transferring file ownership to root makes the files inaccessible to normal \
             users and may break applications that need to write to those files. Services \
             running as non-root users will lose access.\n\n\
             Check who currently owns the file:\n  \
             ls -la <path>\n\n\
             Consider using group ownership instead:\n  \
             chgrp <group> <path>"
        ),
        // setfacl with dangerous patterns
        destructive_pattern!(
            "setfacl-all",
            r"setfacl\s+.*-[rR].*\s+/(?:$|bin|boot|dev|etc|lib|lib64|opt|proc|root|run|sbin|srv|sys|usr|var)\b",
            "setfacl -R on system directories can modify access control across the filesystem.",
            Critical,
            "Recursively modifying ACLs on system directories changes fine-grained access \
             control for every file in the tree. This can override traditional Unix \
             permissions and grant or revoke access in unexpected ways, breaking services \
             and security boundaries.\n\n\
             Review current ACLs first:\n  \
             getfacl <path>\n\n\
             Apply to a specific file instead of recursively:\n  \
             setfacl -m u:<user>:rwx <specific-file>"
        ),
    ]
}
