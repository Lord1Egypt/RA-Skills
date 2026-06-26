---
name: france-cinemas
description: Search French cinema establishments using the open data.culture.gouv.fr API. Query by city, region, proximity, screen count, Art et Essai label, and multiplex status. No API key required.
---

# France Cinemas (No API key)

Search and explore the official French government dataset of cinema establishments. The dataset contains 2,061 cinemas with screen counts, seat capacity, attendance figures, Art et Essai classification, geographic coordinates, and more.

Data source: Ministere de la Culture, updated periodically. Licence Ouverte / Open Licence.

## Quick Reference

| Action | Endpoint |
|--------|----------|
| Search by city | `?where=search(commune,"Lyon")` |
| Search by name | `?where=search(nom,"Gaumont")` |
| Nearby cinemas | `?where=within_distance(geolocalisation,geom'POINT(lon lat)',10km)` |
| Art et Essai only | `?where=ae="AE"` |
| Multiplexes only | `?where=multiplexe="OUI"` |
| By region | `?where=region_administrative="ILE DE FRANCE"` |
| Top by attendance | `?order_by=entrees_2022 desc&limit=10` |

Base URL for all queries:

```
https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/records
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `nom` | text | Cinema name |
| `commune` | text | City name |
| `dep` | text | Department number (e.g. "75") |
| `region_administrative` | text | Region (e.g. "ILE DE FRANCE") |
| `adresse` | text | Street address |
| `code_insee` | text | INSEE municipality code |
| `population_commune` | int | City population |
| `ecrans` | int | Number of screens |
| `fauteuils` | int | Total seats |
| `entrees_2022` | int | Admissions in 2022 |
| `ae` | text | Art et Essai label ("AE" or empty) |
| `genre` | text | Venue type ("Fixe", "Itinerant", "Saisonnier") |
| `multiplexe` | text | Multiplex status ("OUI", "NON") |
| `zone_de_la_commune` | text | Urban zone ("U" urban, "R" rural) |
| `geolocalisation` | geo_point | Latitude/longitude coordinates |
| `nombre_de_films_programmes` | int | Number of films screened |
| `nombre_de_films_inedits` | int | Number of first-run films |
| `nombre_de_films_en_semaine_1` | int | Films in their first week |
| `pdm_en_entrees` | float | Market share by admissions |

## Search by City or Name

Use the `search()` function for full-text matching on a specific field.

```
GET /api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/records?where=search(commune,"Marseille")&limit=20
```

Combine with other filters using `AND`:

```
?where=search(commune,"Paris") AND ecrans>=5
```

Search by cinema name:

```
?where=search(nom,"Pathe")
```

## Search by Region or Department

Region values are uppercase. Common values: ILE DE FRANCE, AUVERGNE-RHONE-ALPES, PROVENCE-ALPES-COTE D'AZUR, OCCITANIE, NOUVELLE-AQUITAINE, HAUTS-DE-FRANCE, GRAND EST, PAYS DE LA LOIRE, BRETAGNE, NORMANDIE, BOURGOGNE-FRANCHE-COMTE, CENTRE-VAL DE LOIRE, CORSE, OUTRE-MER.

```
?where=region_administrative="BRETAGNE"&limit=50
```

By department number:

```
?where=dep="75"
```

## Geographic Proximity Search

Find cinemas within a radius of a point. Coordinates use longitude first, then latitude (POINT(lon lat)).

```
?where=within_distance(geolocalisation, geom'POINT(2.3522 48.8566)', 5km)
```

This returns cinemas within 5 km of central Paris. Supported units: `m`, `km`, `mi`, `yd`, `ft`.

Combine with other filters:

```
?where=within_distance(geolocalisation, geom'POINT(2.3522 48.8566)', 10km) AND ae="AE"
```

## Filter by Type

Art et Essai cinemas (independent/arthouse):

```
?where=ae="AE"
```

Multiplexes (8+ screens):

```
?where=multiplexe="OUI"
```

Fixed venues only (excludes itinerant and seasonal):

```
?where=genre="Fixe"
```

## Sorting and Pagination

Sort by any numeric field. Use `desc` for descending.

```
?order_by=entrees_2022 desc&limit=10
```

Paginate with `offset`:

```
?limit=20&offset=40
```

Maximum `limit` is 100 per request. Use `offset` to iterate through all results.

## Selecting Fields

Return only specific fields to reduce response size:

```
?select=nom,commune,ecrans,fauteuils,entrees_2022&limit=10
```

## Aggregation

Group and aggregate data:

```
?select=region_administrative,count(*) as total,sum(ecrans) as total_screens&group_by=region_administrative&order_by=total desc
```

## Combining Filters

Build complex queries with AND/OR:

```
?where=region_administrative="BRETAGNE" AND ecrans>=3 AND ae="AE"&order_by=entrees_2022 desc
```

Large cinemas (10+ screens) in a city:

```
?where=search(commune,"Lyon") AND ecrans>=10&select=nom,commune,ecrans,fauteuils
```

## Response Format

The API returns JSON. Each response has:

```json
{
  "total_count": 42,
  "results": [
    {
      "nom": "CINEMA EXAMPLE",
      "commune": "PARIS",
      "ecrans": 12,
      "fauteuils": 2800,
      "entrees_2022": 450000,
      "geolocalisation": { "lat": 48.856, "lon": 2.352 },
      ...
    }
  ]
}
```

`total_count` gives the total matching records (useful for pagination). `results` contains the matching cinema records.

## Common Recipes

Find the biggest cinema in France:

```
?order_by=fauteuils desc&limit=1&select=nom,commune,ecrans,fauteuils,entrees_2022
```

All Art et Essai cinemas in Paris:

```
?where=dep="75" AND ae="AE"&order_by=nom asc
```

Cinemas near a user's location (replace coordinates):

```
?where=within_distance(geolocalisation, geom'POINT(USER_LON USER_LAT)', 15km)&order_by=entrees_2022 desc&limit=10
```

Rural cinemas with high attendance:

```
?where=zone_de_la_commune="R" AND entrees_2022>50000&order_by=entrees_2022 desc
```

Summary statistics by region:

```
?select=region_administrative,count(*) as cinemas,sum(ecrans) as screens,sum(fauteuils) as seats&group_by=region_administrative&order_by=cinemas desc
```

## Troubleshooting

### No results returned
Check that text values are uppercase. Region and city names in this dataset use uppercase (e.g., "LYON" not "Lyon"). The `search()` function is case-insensitive, but exact equality checks are not.

### Invalid query syntax
ODSQL uses double quotes for string values in `where` clauses. Single quotes are only used for geometry literals (`geom'POINT(...)'`).

### Pagination limit
The API returns at most 100 records per request. To retrieve all matching records, loop with `offset` increments of your `limit` value until `results` is empty.
