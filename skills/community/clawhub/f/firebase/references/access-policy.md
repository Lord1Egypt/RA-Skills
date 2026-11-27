# Firebase access policy

An access policy limits which endpoints Firebase connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/firebase#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Firebase: its 18 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create firebase --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1beta1/projects/{id}/androidApps"},
    {"method": "GET", "path": "v1beta1/projects/{id}/androidApps/{id}"},
    {"method": "GET", "path": "v1beta1/projects/{id}/androidApps/{id}/config"},
    {"method": "GET", "path": "v1beta1/projects/{id}/androidApps/{id}/sha"},
    {"method": "GET", "path": "v1beta1/projects/{id}/availableLocations"},
    {"method": "GET", "path": "v1beta1/availableProjects"},
    {"method": "GET", "path": "v1beta1/projects/{id}/iosApps"},
    {"method": "GET", "path": "v1beta1/projects/{id}/iosApps/{id}"},
    {"method": "GET", "path": "v1beta1/projects/{id}/iosApps/{id}/config"},
    {"method": "GET", "path": "v1beta1/operations/{id}"},
    {"method": "GET", "path": "v1beta1/projects"},
    {"method": "GET", "path": "v1beta1/projects/{id}"},
    {"method": "GET", "path": "v1beta1/projects/{id}/adminSdkConfig"},
    {"method": "GET", "path": "v1beta1/projects/{id}/analyticsDetails"},
    {"method": "GET", "path": "v1beta1/projects/{id}:searchApps"},
    {"method": "GET", "path": "v1beta1/projects/{id}/webApps"},
    {"method": "GET", "path": "v1beta1/projects/{id}/webApps/{id}"},
    {"method": "GET", "path": "v1beta1/projects/{id}/webApps/{id}/config"}
  ],
  "deny": []
}
```

## Endpoints

The Firebase endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1beta1/projects/{id}/androidApps | read | androidApps | Lists each AndroidApp associated with the specified FirebaseProject. |
| POST | v1beta1/projects/{id}/androidApps | write | androidApps | Requests the creation of a new AndroidApp in the specified FirebaseProject. |
| GET | v1beta1/projects/{id}/androidApps/{id} | read | androidApps | Gets the specified AndroidApp. |
| PATCH | v1beta1/projects/{id}/androidApps/{id} | write | androidApps | Updates the attributes of the specified AndroidApp. |
| GET | v1beta1/projects/{id}/androidApps/{id}/config | read | androidApps | Gets the configuration artifact associated with the specified AndroidApp. |
| GET | v1beta1/projects/{id}/androidApps/{id}/sha | read | androidApps | Lists the SHA-1 and SHA-256 certificates for the specified AndroidApp. |
| POST | v1beta1/projects/{id}/androidApps/{id}/sha | write | androidApps | Adds a ShaCertificate to the specified AndroidApp. |
| DELETE | v1beta1/projects/{id}/androidApps/{id}/sha/{id} | write | androidApps | Removes a ShaCertificate from the specified AndroidApp. |
| POST | v1beta1/projects/{id}/androidApps/{id}:remove | write | androidApps | Removes the specified AndroidApp from the FirebaseProject. |
| POST | v1beta1/projects/{id}/androidApps/{id}:undelete | write | androidApps | Restores the specified AndroidApp to the FirebaseProject. |
| GET | v1beta1/projects/{id}/availableLocations | read | availableLocations | **DECOMMISSIONED.** **If called, this endpoint will return a 404 error.** _Instead, use the applicable resource-specific REST API (or associated documentation,  |
| GET | v1beta1/availableProjects | read | availableProjects | Lists each [Google Cloud `Project`](https://cloud.google.com/resource-manager/reference/rest/v1/projects) that can have Firebase resources added and Firebase se |
| POST | v1beta1/projects/{id}/defaultLocation:finalize | write | defaultLocation | **DECOMMISSIONED.** **If called, this endpoint will return a 404 error.** _Instead, use the applicable resource-specific REST API to set the location for each r |
| GET | v1beta1/projects/{id}/iosApps | read | iosApps | Lists each IosApp associated with the specified FirebaseProject. |
| POST | v1beta1/projects/{id}/iosApps | write | iosApps | Requests the creation of a new IosApp in the specified FirebaseProject. |
| GET | v1beta1/projects/{id}/iosApps/{id} | read | iosApps | Gets the specified IosApp. |
| PATCH | v1beta1/projects/{id}/iosApps/{id} | write | iosApps | Updates the attributes of the specified IosApp. |
| GET | v1beta1/projects/{id}/iosApps/{id}/config | read | iosApps | Gets the configuration artifact associated with the specified IosApp. |
| POST | v1beta1/projects/{id}/iosApps/{id}:remove | write | iosApps | Removes the specified IosApp from the FirebaseProject. |
| POST | v1beta1/projects/{id}/iosApps/{id}:undelete | write | iosApps | Restores the specified IosApp to the FirebaseProject. |
| GET | v1beta1/operations/{id} | read | operations | Gets the latest state of a long-running operation. |
| GET | v1beta1/projects | read | projects | Lists each FirebaseProject accessible to the caller. |
| GET | v1beta1/projects/{id} | read | projects | Gets the specified FirebaseProject. |
| PATCH | v1beta1/projects/{id} | write | projects | Updates the attributes of the specified FirebaseProject. |
| GET | v1beta1/projects/{id}/adminSdkConfig | read | projects | Gets the configuration artifact associated with the specified FirebaseProject, which can be used by servers to simplify initialization. |
| GET | v1beta1/projects/{id}/analyticsDetails | read | projects | Gets the Google Analytics details currently associated with the specified FirebaseProject. |
| POST | v1beta1/projects/{id}:addFirebase | write | projects | Adds Firebase resources and enables Firebase services in the specified existing [Google Cloud `Project`](https://cloud.google.com/resource-manager/reference/res |
| POST | v1beta1/projects/{id}:addGoogleAnalytics | write | projects | Links the specified FirebaseProject with an existing [Google Analytics account](http://www.google.com/analytics/). |
| POST | v1beta1/projects/{id}:removeAnalytics | write | projects | Unlinks the specified FirebaseProject from its Google Analytics account. |
| GET | v1beta1/projects/{id}:searchApps | read | projects | Lists all available Apps for the specified FirebaseProject. |
| GET | v1beta1/projects/{id}/webApps | read | webApps | Lists each WebApp associated with the specified FirebaseProject. |
| POST | v1beta1/projects/{id}/webApps | write | webApps | Requests the creation of a new WebApp in the specified FirebaseProject. |
| GET | v1beta1/projects/{id}/webApps/{id} | read | webApps | Gets the specified WebApp. |
| PATCH | v1beta1/projects/{id}/webApps/{id} | write | webApps | Updates the attributes of the specified WebApp. |
| GET | v1beta1/projects/{id}/webApps/{id}/config | read | webApps | Gets the configuration artifact associated with the specified WebApp. |
| POST | v1beta1/projects/{id}/webApps/{id}:remove | write | webApps | Removes the specified WebApp from the FirebaseProject. |
| POST | v1beta1/projects/{id}/webApps/{id}:undelete | write | webApps | Restores the specified WebApp to the FirebaseProject. |
