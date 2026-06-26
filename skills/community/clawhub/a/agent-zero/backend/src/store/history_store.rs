use crate::models::history::{HistoryEntry, HistoryField};
use sqlx::{Row, SqlitePool};

/// Record a field value change for a listing.
pub async fn insert_change(
    pool: &SqlitePool,
    listing_id: i64,
    field_name: HistoryField,
    old_value: Option<&str>,
    new_value: Option<&str>,
) -> Result<(), sqlx::Error> {
    sqlx::query(
        "INSERT INTO listing_history (listing_id, field_name, old_value, new_value)
         VALUES (?, ?, ?, ?)",
    )
    .bind(listing_id)
    .bind(field_name.to_string())
    .bind(old_value)
    .bind(new_value)
    .execute(pool)
    .await?;
    Ok(())
}

/// Return all history entries for a listing, newest first.
pub async fn list_history(
    pool: &SqlitePool,
    listing_id: i64,
) -> Result<Vec<HistoryEntry>, sqlx::Error> {
    let rows = sqlx::query(
        "SELECT id, listing_id, field_name, old_value, new_value, changed_at
         FROM listing_history WHERE listing_id = ? ORDER BY changed_at DESC",
    )
    .bind(listing_id)
    .fetch_all(pool)
    .await?;

    rows.iter()
        .map(|r| -> Result<HistoryEntry, sqlx::Error> {
            let field_name_str: String = r.get("field_name");
            Ok(HistoryEntry {
                id: r.get("id"),
                listing_id: r.get("listing_id"),
                field_name: field_name_str.parse().map_err(sqlx::Error::Protocol)?,
                old_value: r.get("old_value"),
                new_value: r.get("new_value"),
                changed_at: r.get("changed_at"),
            })
        })
        .collect()
}
