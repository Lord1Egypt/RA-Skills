# Modes and parameters

Read this reference only when selecting a non-default mode or mapping advanced fields.

## Username Mode Parameters

Use this section only when the user chooses `username`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `username` | Yes | `zoobarcelona` | Instagram username. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple Instagram profile username groups? If yes, provide multiple `username` values."

Username mode handling:

- Trim leading and trailing whitespace from `username`.
- `username` cannot be empty.
- Submit `spider_id=ins_profiles_by-username`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"username":"zoobarcelona"}]
```

## Profile URL Mode Parameters

Use this section only when the user chooses `profileurl`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `profileurl` | Yes | `https://www.instagram.com/cats_of_world_/` | Instagram profile URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple Instagram profile URL groups? If yes, provide multiple `profileurl` values."

Profile URL mode handling:

- Trim leading and trailing whitespace from `profileurl`.
- `profileurl` cannot be empty.
- `profileurl` must start with `https://www.instagram.com/`.
- Submit `spider_id=ins_profiles_by-profileurl`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"profileurl":"https://www.instagram.com/cats_of_world_/"}]
```
