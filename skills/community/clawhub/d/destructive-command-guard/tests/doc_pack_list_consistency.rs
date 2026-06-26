use destructive_command_guard::packs::PackRegistry;
use std::collections::BTreeSet;

fn read_repo_file(path: &str) -> std::io::Result<String> {
    let repo_root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let full_path = repo_root.join(path);
    std::fs::read_to_string(&full_path)
}

fn registry_pack_ids() -> BTreeSet<&'static str> {
    PackRegistry::new().all_pack_ids().into_iter().collect()
}

#[test]
fn docs_packs_index_matches_registry_ids() -> std::io::Result<()> {
    let expected = registry_pack_ids();
    let docs = read_repo_file("docs/packs/README.md")?;

    let mut found: BTreeSet<String> = BTreeSet::new();
    for line in docs.lines() {
        let trimmed = line.trim();
        // Match old format: - `pack_id`
        if let Some(rest) = trimmed
            .strip_prefix("- `")
            .and_then(|rest| rest.strip_suffix('`'))
        {
            found.insert(rest.to_string());
        }
        // Match new format: - [`pack_id`](file.md#anchor)
        else if let Some(rest) = trimmed.strip_prefix("- [`") {
            if let Some(pack_id) = rest.split('`').next() {
                found.insert(pack_id.to_string());
            }
        }
    }

    let missing: Vec<String> = expected
        .iter()
        .filter(|id| !found.contains(**id))
        .map(ToString::to_string)
        .collect();
    let extra: Vec<String> = found
        .iter()
        .filter(|id| !expected.contains(id.as_str()))
        .cloned()
        .collect();

    assert!(
        missing.is_empty(),
        "docs/packs/README.md is missing pack ids:\n{}",
        missing.join("\n")
    );
    assert!(
        extra.is_empty(),
        "docs/packs/README.md contains unknown pack ids:\n{}",
        extra.join("\n")
    );

    Ok(())
}

#[test]
fn readme_lists_all_registry_pack_ids() -> std::io::Result<()> {
    let expected = registry_pack_ids();
    let readme = read_repo_file("README.md")?;

    let missing: Vec<String> = expected
        .iter()
        .filter(|id| !readme.contains(&format!("`{id}`")))
        .map(ToString::to_string)
        .collect();

    assert!(
        missing.is_empty(),
        "README.md is missing pack ids:\n{}",
        missing.join("\n")
    );

    Ok(())
}
