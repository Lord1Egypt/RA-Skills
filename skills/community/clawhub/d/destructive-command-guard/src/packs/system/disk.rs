//! Disk patterns - protections against destructive disk operations.
//!
//! This includes patterns for:
//! - dd to block devices
//! - fdisk/parted operations
//! - mkfs (formatting)
//! - mount/umount operations
//! - mdadm RAID management
//! - btrfs filesystem operations
//! - dmsetup device-mapper operations
//! - nbd-client network block device
//! - LVM destructive commands (pvremove, vgremove, lvremove, etc.)

use crate::packs::{DestructivePattern, Pack, SafePattern};
use crate::{destructive_pattern, safe_pattern};

/// Create the Disk pack.
#[must_use]
pub fn create_pack() -> Pack {
    Pack {
        id: "system.disk".to_string(),
        name: "Disk Operations",
        description: "Protects against destructive disk operations like dd to devices, \
                      mkfs, partition table modifications, RAID management, \
                      btrfs/LVM/device-mapper operations, and network block devices",
        keywords: &[
            "dd",
            "fdisk",
            "mkfs",
            "parted",
            "mount",
            "wipefs",
            "/dev/",
            "mdadm",
            "btrfs",
            "dmsetup",
            "nbd-client",
            "pvremove",
            "vgremove",
            "lvremove",
            "vgreduce",
            "lvreduce",
            "lvresize",
            "pvmove",
        ],
        safe_patterns: create_safe_patterns(),
        destructive_patterns: create_destructive_patterns(),
        keyword_matcher: None,
        safe_regex_set: None,
        safe_regex_set_is_complete: false,
    }
}

fn create_safe_patterns() -> Vec<SafePattern> {
    vec![
        // dd to regular files is generally safe
        safe_pattern!("dd-file-out", r"dd\s+.*of=[^/\s]+\."),
        // dd to /dev/null|zero|full is safe (discard output)
        safe_pattern!("dd-discard", r"dd\s+.*of=/dev/(?:null|zero|full)(?:\s|$)"),
        // lsblk is safe (read-only)
        safe_pattern!("lsblk", r"\blsblk\b"),
        // fdisk -l (list) is safe
        safe_pattern!("fdisk-list", r"fdisk\s+-l"),
        // parted print is safe
        safe_pattern!("parted-print", r"parted\s+.*print"),
        // blkid is safe (read-only)
        safe_pattern!("blkid", r"\bblkid\b"),
        // df is safe
        safe_pattern!("df", r"\bdf\b"),
        // mount (without arguments, just list)
        safe_pattern!("mount-list", r"\bmount\s*$"),
        // --- mdadm safe patterns ---
        // mdadm --detail (read-only inspection)
        safe_pattern!("mdadm-detail", r"mdadm\s+--detail\b"),
        // mdadm --examine (read-only superblock inspection)
        safe_pattern!("mdadm-examine", r"mdadm\s+--examine\b"),
        // mdadm --query (read-only query)
        safe_pattern!("mdadm-query", r"mdadm\s+--query\b"),
        // mdadm -Q (short form of --query)
        safe_pattern!("mdadm-query-short", r"mdadm\s+-Q\b"),
        // mdadm --scan (scan for arrays, read-only)
        safe_pattern!("mdadm-scan", r"mdadm\s+--scan\b"),
        // --- btrfs safe patterns ---
        // btrfs subvolume list (read-only)
        safe_pattern!("btrfs-subvolume-list", r"btrfs\s+subvolume\s+list\b"),
        // btrfs subvolume show (read-only)
        safe_pattern!("btrfs-subvolume-show", r"btrfs\s+subvolume\s+show\b"),
        // btrfs filesystem show (read-only)
        safe_pattern!("btrfs-filesystem-show", r"btrfs\s+filesystem\s+show\b"),
        // btrfs filesystem df (read-only)
        safe_pattern!("btrfs-filesystem-df", r"btrfs\s+filesystem\s+df\b"),
        // btrfs filesystem usage (read-only)
        safe_pattern!("btrfs-filesystem-usage", r"btrfs\s+filesystem\s+usage\b"),
        // btrfs device stats (read-only)
        safe_pattern!("btrfs-device-stats", r"btrfs\s+device\s+stats\b"),
        // btrfs property get/list (read-only)
        safe_pattern!("btrfs-property-get", r"btrfs\s+property\s+(?:get|list)\b"),
        // btrfs scrub status (read-only)
        safe_pattern!("btrfs-scrub-status", r"btrfs\s+scrub\s+status\b"),
        // --- dmsetup safe patterns ---
        // dmsetup ls (list devices)
        safe_pattern!("dmsetup-ls", r"dmsetup\s+ls\b"),
        // dmsetup status (show status)
        safe_pattern!("dmsetup-status", r"dmsetup\s+status\b"),
        // dmsetup info (show info)
        safe_pattern!("dmsetup-info", r"dmsetup\s+info\b"),
        // dmsetup table (show mapping table)
        safe_pattern!("dmsetup-table", r"dmsetup\s+table\b"),
        // dmsetup deps (show dependencies)
        safe_pattern!("dmsetup-deps", r"dmsetup\s+deps\b"),
        // --- nbd-client safe patterns ---
        // nbd-client -l (list exports)
        safe_pattern!("nbd-client-list", r"nbd-client\s+-l\b"),
        // nbd-client -check (check connection)
        safe_pattern!("nbd-client-check", r"nbd-client\s+.*-check\b"),
        // --- LVM safe patterns (read-only) ---
        // lvs, vgs, pvs (list commands)
        safe_pattern!("lvm-list", r"\b(?:lvs|vgs|pvs)\b"),
        // lvdisplay, vgdisplay, pvdisplay (display commands)
        safe_pattern!("lvm-display", r"\b(?:lvdisplay|vgdisplay|pvdisplay)\b"),
        // lvscan, vgscan, pvscan (scan commands)
        safe_pattern!("lvm-scan", r"\b(?:lvscan|vgscan|pvscan)\b"),
    ]
}

fn create_destructive_patterns() -> Vec<DestructivePattern> {
    vec![
        // dd to block devices
        destructive_pattern!(
            "dd-device",
            r"dd\s+.*of=/dev/",
            "dd to a block device will OVERWRITE all data on that device. Extremely dangerous!"
        ),
        // dd with if=/dev/zero or if=/dev/urandom to devices
        destructive_pattern!(
            "dd-wipe",
            r"dd\s+.*if=/dev/(?:zero|urandom|random).*of=/dev/",
            "dd from /dev/zero or /dev/urandom to a device will WIPE all data!"
        ),
        // fdisk (partition editing)
        destructive_pattern!(
            "fdisk-edit",
            r"fdisk\s+/dev/(?!.*-l)",
            "fdisk can modify partition tables and cause data loss."
        ),
        // parted (except print)
        destructive_pattern!(
            "parted-modify",
            r"parted\s+/dev/\S+\s+(?!print)",
            "parted can modify partition tables and cause data loss."
        ),
        // mkfs (format filesystem)
        destructive_pattern!(
            "mkfs",
            r"mkfs(?:\.[a-z0-9]+)?\s+",
            "mkfs formats a partition/device and ERASES all existing data."
        ),
        // wipefs
        destructive_pattern!(
            "wipefs",
            r"wipefs\s+",
            "wipefs removes filesystem signatures. Use with extreme caution."
        ),
        // mount with potentially dangerous options
        destructive_pattern!(
            "mount-bind-root",
            r"mount\s+.*--bind\s+.*\s+/(?:$|[^a-z])",
            "mount --bind to root directory can have system-wide effects."
        ),
        // umount -f (force)
        destructive_pattern!(
            "umount-force",
            r"umount\s+.*-[a-z]*f",
            "umount -f force unmounts which may cause data loss if device is in use."
        ),
        // losetup can be dangerous
        destructive_pattern!(
            "losetup-device",
            r"losetup\s+/dev/loop",
            "losetup modifies loop device associations. Verify before proceeding."
        ),
        // --- mdadm destructive patterns ---
        // mdadm --stop (stops a running RAID array)
        destructive_pattern!(
            "mdadm-stop",
            r"mdadm\s+(?:.*\s+)?(?:--stop|-S)\b",
            "mdadm --stop shuts down a RAID array. Data may become inaccessible."
        ),
        // mdadm --remove (removes a device from an array)
        destructive_pattern!(
            "mdadm-remove",
            r"mdadm\s+(?:.*\s+)?--remove\b",
            "mdadm --remove removes a drive from a RAID array. May cause data loss if redundancy is lost."
        ),
        // mdadm --fail (marks a device as failed)
        destructive_pattern!(
            "mdadm-fail",
            r"mdadm\s+(?:.*\s+)?(?:--fail|-f)\b",
            "mdadm --fail marks a device as failed. Use only for intentional drive replacement."
        ),
        // mdadm --zero-superblock (wipes RAID superblock)
        destructive_pattern!(
            "mdadm-zero-superblock",
            r"mdadm\s+(?:.*\s+)?--zero-superblock\b",
            "mdadm --zero-superblock PERMANENTLY erases RAID metadata. Array cannot be reassembled."
        ),
        // mdadm --create (creates a new array, can overwrite existing data)
        destructive_pattern!(
            "mdadm-create",
            r"mdadm\s+(?:.*\s+)?(?:--create|-C)\b",
            "mdadm --create initializes a new RAID array, ERASING existing data on member devices."
        ),
        // mdadm --grow with dangerous options
        destructive_pattern!(
            "mdadm-grow",
            r"mdadm\s+(?:.*\s+)?--grow\b",
            "mdadm --grow reshapes a RAID array. Interruption can cause data loss. Backup first."
        ),
        // --- btrfs destructive patterns ---
        // btrfs subvolume delete
        destructive_pattern!(
            "btrfs-subvolume-delete",
            r"btrfs\s+subvolume\s+delete\b",
            "btrfs subvolume delete PERMANENTLY removes a subvolume and all its data."
        ),
        // btrfs device remove/delete
        destructive_pattern!(
            "btrfs-device-remove",
            r"btrfs\s+device\s+(?:remove|delete)\b",
            "btrfs device remove redistributes data off a device. Interruption causes data loss."
        ),
        // btrfs device add (can be dangerous with wrong device)
        destructive_pattern!(
            "btrfs-device-add",
            r"btrfs\s+device\s+add\b",
            "btrfs device add incorporates a device into the filesystem. Verify the device is correct."
        ),
        // btrfs balance start (can be very disruptive)
        destructive_pattern!(
            "btrfs-balance",
            r"btrfs\s+balance\s+start\b",
            "btrfs balance redistributes data across devices. Can be slow and disruptive."
        ),
        // btrfs check --repair (dangerous, can corrupt filesystem)
        destructive_pattern!(
            "btrfs-check-repair",
            r"btrfs\s+check\s+(?:.*\s+)?--repair\b",
            "btrfs check --repair is DANGEROUS and can cause data loss. Backup first!"
        ),
        // btrfs rescue (emergency operations)
        destructive_pattern!(
            "btrfs-rescue",
            r"btrfs\s+rescue\b",
            "btrfs rescue operations modify filesystem metadata. Use only as last resort."
        ),
        // btrfs filesystem resize (can shrink)
        destructive_pattern!(
            "btrfs-filesystem-resize",
            r"btrfs\s+filesystem\s+resize\b",
            "btrfs filesystem resize can shrink a filesystem. Data loss if size is too small."
        ),
        // --- dmsetup destructive patterns ---
        // dmsetup remove (removes a device-mapper device)
        destructive_pattern!(
            "dmsetup-remove",
            r"dmsetup\s+remove\b",
            "dmsetup remove detaches a device-mapper device. May cause data loss if in use."
        ),
        // dmsetup remove_all (removes ALL device-mapper devices)
        destructive_pattern!(
            "dmsetup-remove-all",
            r"dmsetup\s+remove_all\b",
            "dmsetup remove_all removes ALL device-mapper devices. Extremely dangerous!"
        ),
        // dmsetup wipe_table (replaces table with error target)
        destructive_pattern!(
            "dmsetup-wipe-table",
            r"dmsetup\s+wipe_table\b",
            "dmsetup wipe_table replaces the device table, causing all I/O to fail."
        ),
        // dmsetup clear (clears the table)
        destructive_pattern!(
            "dmsetup-clear",
            r"dmsetup\s+clear\b",
            "dmsetup clear removes the mapping table from a device."
        ),
        // dmsetup load (loads a new table)
        destructive_pattern!(
            "dmsetup-load",
            r"dmsetup\s+load\b",
            "dmsetup load changes device mapping. Verify the new table is correct."
        ),
        // dmsetup create (creates a new device)
        destructive_pattern!(
            "dmsetup-create",
            r"dmsetup\s+create\b",
            "dmsetup create sets up a new device-mapper device. Verify parameters carefully."
        ),
        // --- nbd-client destructive patterns ---
        // nbd-client -d (disconnect)
        destructive_pattern!(
            "nbd-client-disconnect",
            r"nbd-client\s+(?:.*\s+)?-d\b",
            "nbd-client -d disconnects a network block device. Data loss if not properly unmounted."
        ),
        // nbd-client connect (can overwrite existing data)
        destructive_pattern!(
            "nbd-client-connect",
            r"nbd-client\s+\S+\s+\d+\s+/dev/nbd",
            "nbd-client connecting a device can expose or overwrite data. Verify server and device."
        ),
        // --- LVM destructive patterns ---
        // pvremove (removes physical volume)
        destructive_pattern!(
            "pvremove",
            r"\bpvremove\b",
            "pvremove ERASES LVM metadata from a physical volume. Data becomes inaccessible."
        ),
        // vgremove (removes volume group)
        destructive_pattern!(
            "vgremove",
            r"\bvgremove\b",
            "vgremove DELETES a volume group and all logical volumes within it."
        ),
        // lvremove (removes logical volume)
        destructive_pattern!(
            "lvremove",
            r"\blvremove\b",
            "lvremove PERMANENTLY deletes a logical volume and ALL its data."
        ),
        // vgreduce (removes PV from VG)
        destructive_pattern!(
            "vgreduce",
            r"\bvgreduce\b",
            "vgreduce removes a physical volume from a volume group. Data may be lost."
        ),
        // lvreduce (shrinks logical volume)
        destructive_pattern!(
            "lvreduce",
            r"\blvreduce\b",
            "lvreduce SHRINKS a logical volume. Data loss if filesystem isn't resized first!"
        ),
        // lvresize with shrink (can lose data)
        destructive_pattern!(
            "lvresize-shrink",
            r"lvresize\s+(?:.*\s+)?(?:-L\s*-|-l\s*-|--size\s+\S*-)",
            "lvresize with negative size SHRINKS the volume. Resize filesystem first or lose data!"
        ),
        // pvmove (moves data between PVs, interruptible = bad)
        destructive_pattern!(
            "pvmove",
            r"\bpvmove\b",
            "pvmove migrates data between physical volumes. Do NOT interrupt or data may be lost."
        ),
        // lvcreate with snapshot removal
        destructive_pattern!(
            "lvconvert-merge",
            r"lvconvert\s+(?:.*\s+)?--merge\b",
            "lvconvert --merge reverts LV to snapshot state, discarding changes since snapshot."
        ),
    ]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn wipefs_is_reachable_via_keywords() {
        let pack = create_pack();
        assert!(
            pack.might_match("wipefs --all somefile.img"),
            "wipefs should be included in pack keywords to prevent false negatives"
        );
        let matched = pack
            .check("wipefs --all somefile.img")
            .expect("wipefs should be blocked by disk pack");
        assert_eq!(matched.name, Some("wipefs"));
    }

    #[test]
    fn keyword_absent_skips_pack() {
        let pack = create_pack();
        assert!(!pack.might_match("echo hello"));
        assert!(pack.check("echo hello").is_none());
    }
}
