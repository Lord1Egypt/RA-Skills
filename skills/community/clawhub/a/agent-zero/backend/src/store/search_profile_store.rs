use crate::models::search_profile::SearchProfile;
use sqlx::{Row, SqlitePool};

/// Insert a new search profile and return it. Position is set to max+1 so it appears last.
pub async fn create(pool: &SqlitePool, title: &str, description: &str) -> Result<SearchProfile, sqlx::Error> {
    let row = sqlx::query(
        r#"INSERT INTO search_profiles (title, description, position)
           VALUES (?, ?, COALESCE((SELECT MAX(position) FROM search_profiles), -1) + 1)
           RETURNING id, title, description, position, created_at, updated_at"#,
    )
    .bind(title)
    .bind(description)
    .fetch_one(pool)
    .await?;

    Ok(SearchProfile {
        id: row.get("id"),
        title: row.get("title"),
        description: row.get("description"),
        position: row.get("position"),
        created_at: row.get("created_at"),
        updated_at: row.get("updated_at"),
        listing_count: 0,
    })
}

/// List all search profiles ordered by position, with a count of listings in each.
pub async fn list_all(pool: &SqlitePool) -> Result<Vec<SearchProfile>, sqlx::Error> {
    let rows = sqlx::query(
        r#"SELECT s.id, s.title, s.description, s.position, s.created_at, s.updated_at,
                  COUNT(l.id) AS listing_count
           FROM search_profiles s
           LEFT JOIN listings l ON l.search_profile_id = s.id
           GROUP BY s.id
           ORDER BY s.position ASC"#,
    )
    .fetch_all(pool)
    .await?;

    Ok(rows
        .iter()
        .map(|r| SearchProfile {
            id: r.get("id"),
            title: r.get("title"),
            description: r.get("description"),
            position: r.get("position"),
            created_at: r.get("created_at"),
            updated_at: r.get("updated_at"),
            listing_count: r.get("listing_count"),
        })
        .collect())
}

/// Get a single search profile by ID.
pub async fn get_by_id(pool: &SqlitePool, id: i64) -> Result<SearchProfile, sqlx::Error> {
    let row = sqlx::query(
        r#"SELECT s.id, s.title, s.description, s.position, s.created_at, s.updated_at,
                  COUNT(l.id) AS listing_count
           FROM search_profiles s
           LEFT JOIN listings l ON l.search_profile_id = s.id
           WHERE s.id = ?
           GROUP BY s.id"#,
    )
    .bind(id)
    .fetch_one(pool)
    .await?;

    Ok(SearchProfile {
        id: row.get("id"),
        title: row.get("title"),
        description: row.get("description"),
        position: row.get("position"),
        created_at: row.get("created_at"),
        updated_at: row.get("updated_at"),
        listing_count: row.get("listing_count"),
    })
}

/// Update a search profile's title and/or description.
pub async fn update(
    pool: &SqlitePool,
    id: i64,
    title: Option<&str>,
    description: Option<&str>,
) -> Result<SearchProfile, sqlx::Error> {
    if let Some(t) = title {
        sqlx::query("UPDATE search_profiles SET title = ?, updated_at = datetime('now') WHERE id = ?")
            .bind(t)
            .bind(id)
            .execute(pool)
            .await?;
    }
    if let Some(d) = description {
        sqlx::query(
            "UPDATE search_profiles SET description = ?, updated_at = datetime('now') WHERE id = ?",
        )
        .bind(d)
        .bind(id)
        .execute(pool)
        .await?;
    }
    get_by_id(pool, id).await
}

/// Reorder search profiles: accepts a list of IDs in the desired order.
/// Each ID is assigned position = its index in the list.
pub async fn reorder(pool: &SqlitePool, ids: &[i64]) -> Result<(), sqlx::Error> {
    for (pos, id) in ids.iter().enumerate() {
        sqlx::query("UPDATE search_profiles SET position = ?, updated_at = datetime('now') WHERE id = ?")
            .bind(pos as i64)
            .bind(id)
            .execute(pool)
            .await?;
    }
    Ok(())
}

/// Delete a search profile. Listings that belonged to it must be moved first;
/// this function moves them to the first remaining search profile.
pub async fn delete(pool: &SqlitePool, id: i64) -> Result<(), sqlx::Error> {
    // Move listings to the first remaining search profile (by position) if one exists.
    sqlx::query(
        r#"UPDATE listings SET search_profile_id = (
               SELECT id FROM search_profiles WHERE id != ? ORDER BY position ASC LIMIT 1
           ) WHERE search_profile_id = ?"#,
    )
    .bind(id)
    .bind(id)
    .execute(pool)
    .await?;
    sqlx::query("DELETE FROM search_profiles WHERE id = ?")
        .bind(id)
        .execute(pool)
        .await?;
    Ok(())
}
