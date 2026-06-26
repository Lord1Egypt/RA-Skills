use serde::{Deserialize, Deserializer, Serialize, Serializer};
#[cfg(test)]
use ts_rs::TS;
use std::fmt;
use std::str::FromStr;

/// Fields we track in change history.
#[derive(Clone, Debug, PartialEq, Eq)]
#[cfg_attr(test, derive(TS), ts(export, export_to = "../../frontend/src/bindings/"))]
pub enum HistoryField {
    Price,
    MlsNumber,
    ListedDate,
    SourceStatus,
}

impl FromStr for HistoryField {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "price" => Ok(HistoryField::Price),
            "mls_number" => Ok(HistoryField::MlsNumber),
            "listed_date" => Ok(HistoryField::ListedDate),
            "source_status" => Ok(HistoryField::SourceStatus),
            other => Err(format!("unknown history field: {other}")),
        }
    }
}

impl fmt::Display for HistoryField {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(match self {
            HistoryField::Price => "price",
            HistoryField::MlsNumber => "mls_number",
            HistoryField::ListedDate => "listed_date",
            HistoryField::SourceStatus => "source_status",
        })
    }
}

impl Serialize for HistoryField {
    fn serialize<S: Serializer>(&self, s: S) -> Result<S::Ok, S::Error> {
        s.serialize_str(&self.to_string())
    }
}

impl<'de> Deserialize<'de> for HistoryField {
    fn deserialize<D: Deserializer<'de>>(d: D) -> Result<Self, D::Error> {
        let raw = String::deserialize(d)?;
        raw.parse().map_err(serde::de::Error::custom)
    }
}

/// A record of a field value change on a listing (e.g. price went from X to Y).
#[derive(Serialize, Deserialize, Clone)]
#[cfg_attr(test, derive(TS), ts(export, export_to = "../../frontend/src/bindings/"))]
pub struct HistoryEntry {
    pub id: i64,
    pub listing_id: i64,
    pub field_name: HistoryField,
    pub old_value: Option<String>,
    pub new_value: Option<String>,
    pub changed_at: String,
}
