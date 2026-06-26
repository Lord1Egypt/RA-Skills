use crate::models::open_house::{OpenHouse, OpenHouseEvent};
use sqlx::{Row, SqlitePool};

#[cfg(test)]
fn oh(start: &str, end: &str) -> OpenHouseEvent {
    OpenHouseEvent {
        start_time: start.to_string(),
        end_time: Some(end.to_string()),
    }
}

/// Insert open house events for a listing, ignoring duplicates (same listing + start_time).
pub async fn upsert_open_houses(
    pool: &SqlitePool,
    listing_id: i64,
    events: &[OpenHouseEvent],
) -> Result<(), sqlx::Error> {
    for event in events {
        sqlx::query(
            "INSERT INTO open_houses (listing_id, start_time, end_time)
             VALUES (?, ?, ?)
             ON CONFLICT (listing_id, start_time) DO NOTHING",
        )
        .bind(listing_id)
        .bind(&event.start_time)
        .bind(event.end_time.as_deref())
        .execute(pool)
        .await?;
    }
    Ok(())
}

/// Return all open house events for a listing, ordered by start_time ascending.
pub async fn list_open_houses(
    pool: &SqlitePool,
    listing_id: i64,
) -> Result<Vec<OpenHouse>, sqlx::Error> {
    let rows = sqlx::query(
        "SELECT id, listing_id, start_time, end_time, visited, created_at
         FROM open_houses WHERE listing_id = ? ORDER BY start_time ASC",
    )
    .bind(listing_id)
    .fetch_all(pool)
    .await?;

    Ok(rows
        .iter()
        .map(|r| OpenHouse {
            id: r.get("id"),
            listing_id: r.get("listing_id"),
            start_time: r.get("start_time"),
            end_time: r.get("end_time"),
            visited: r.get::<i64, _>("visited") != 0,
            created_at: r.get("created_at"),
        })
        .collect())
}

/// Toggle the visited flag on a single open house event, scoped to the given listing.
///
/// Returns `Ok(false)` if the open house ID does not belong to `listing_id`.
pub async fn patch_open_house_visited(
    pool: &SqlitePool,
    listing_id: i64,
    oh_id: i64,
    visited: bool,
) -> Result<bool, sqlx::Error> {
    let result =
        sqlx::query("UPDATE open_houses SET visited = ? WHERE id = ? AND listing_id = ?")
            .bind(if visited { 1i64 } else { 0i64 })
            .bind(oh_id)
            .bind(listing_id)
            .execute(pool)
            .await?;
    Ok(result.rows_affected() > 0)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::store::property_store;
    use std::sync::atomic::{AtomicUsize, Ordering};

    static TEST_COUNTER: AtomicUsize = AtomicUsize::new(0);

    /// Create a fresh temp SQLite DB (with migrations) and return (pool, listing_id).
    /// Uses an atomic counter so concurrent tests never collide on the same file.
    async fn setup() -> (SqlitePool, i64) {
        let n = TEST_COUNTER.fetch_add(1, Ordering::SeqCst);
        let db_path = std::env::temp_dir()
            .join(format!("agentzero_oh_test_{}_{}.db", std::process::id(), n));
        let database_url = format!("sqlite://{}", db_path.display());
        let pool = property_store::init(&database_url).await;

        // Insert a minimal listing so FK constraints are satisfied.
        let listing_id: i64 = sqlx::query_scalar(
            "INSERT INTO listings (title, description, status, search_profile_id) VALUES ('Test', '', 'Interested', 1) RETURNING id",
        )
        .fetch_one(&pool)
        .await
        .expect("insert listing");

        (pool, listing_id)
    }

    /// Append-only: open houses already in the DB are never deleted when a
    /// refresh upserts a different (or smaller) set.
    #[tokio::test]
    async fn upsert_preserves_expired_entries() {
        let (pool, id) = setup().await;

        // First refresh: two upcoming open houses.
        let first = vec![
            oh("2026-03-07T14:00:00", "2026-03-07T17:00:00"),
            oh("2026-03-08T14:00:00", "2026-03-08T17:00:00"),
        ];
        upsert_open_houses(&pool, id, &first).await.unwrap();

        // Second refresh: the Mar 7 slot expired and is gone from the page;
        // a new Mar 14 slot appeared.
        let second = vec![
            oh("2026-03-08T14:00:00", "2026-03-08T17:00:00"), // already present
            oh("2026-03-14T14:00:00", "2026-03-14T17:00:00"), // new
        ];
        upsert_open_houses(&pool, id, &second).await.unwrap();

        let all = list_open_houses(&pool, id).await.unwrap();
        let start_times: Vec<&str> = all.iter().map(|o| o.start_time.as_str()).collect();

        // All three distinct slots must be present.
        assert!(start_times.contains(&"2026-03-07T14:00:00"), "expired Mar 7 entry was deleted");
        assert!(start_times.contains(&"2026-03-08T14:00:00"), "Mar 8 entry missing");
        assert!(start_times.contains(&"2026-03-14T14:00:00"), "new Mar 14 entry missing");
        assert_eq!(all.len(), 3, "expected exactly 3 entries, got {}", all.len());
    }

    /// Duplicate upserts (same listing + start_time) must not create extra rows.
    #[tokio::test]
    async fn upsert_deduplicates() {
        let (pool, id) = setup().await;

        let events = vec![oh("2026-03-07T14:00:00", "2026-03-07T17:00:00")];
        upsert_open_houses(&pool, id, &events).await.unwrap();
        upsert_open_houses(&pool, id, &events).await.unwrap(); // exact duplicate

        let all = list_open_houses(&pool, id).await.unwrap();
        assert_eq!(all.len(), 1, "duplicate upsert created extra rows");
    }

    /// `visited` can be toggled on and off; the returned bool indicates whether the row was found.
    #[tokio::test]
    async fn patch_visited_toggle() {
        let (pool, id) = setup().await;

        upsert_open_houses(&pool, id, &[oh("2026-03-07T14:00:00", "2026-03-07T17:00:00")])
            .await
            .unwrap();
        let oh_id = list_open_houses(&pool, id).await.unwrap()[0].id;

        assert!(!list_open_houses(&pool, id).await.unwrap()[0].visited, "should start unvisited");

        assert!(patch_open_house_visited(&pool, id, oh_id, true).await.unwrap());
        assert!(list_open_houses(&pool, id).await.unwrap()[0].visited, "should be visited after patch");

        assert!(patch_open_house_visited(&pool, id, oh_id, false).await.unwrap());
        assert!(!list_open_houses(&pool, id).await.unwrap()[0].visited, "should be unvisited after second patch");
    }

    /// `patch_open_house_visited` is scoped to `listing_id`; it must not
    /// affect open houses belonging to a different listing.
    #[tokio::test]
    async fn patch_visited_scoped_to_listing() {
        let (pool, id_a) = setup().await;

        // Create a second listing in the same DB.
        let id_b: i64 = sqlx::query_scalar(
            "INSERT INTO listings (title, description, status, search_profile_id) VALUES ('Other', '', 'Interested', 1) RETURNING id",
        )
        .fetch_one(&pool)
        .await
        .unwrap();

        upsert_open_houses(&pool, id_a, &[oh("2026-03-07T14:00:00", "2026-03-07T17:00:00")])
            .await
            .unwrap();
        let oh_id_a = list_open_houses(&pool, id_a).await.unwrap()[0].id;

        // Trying to patch listing A's open house via listing B's ID must fail (returns false).
        let affected = patch_open_house_visited(&pool, id_b, oh_id_a, true).await.unwrap();
        assert!(!affected, "cross-listing patch should return false");

        // And the row should remain untouched.
        assert!(!list_open_houses(&pool, id_a).await.unwrap()[0].visited);
    }
}
