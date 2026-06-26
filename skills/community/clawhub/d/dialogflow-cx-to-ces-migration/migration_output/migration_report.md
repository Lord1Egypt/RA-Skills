# Dialogflow CX → CES Migration Report

**Source Agent:** carconnect (`3736c564-5b3b-4f93-bbb2-367e7f04e4e8`)
**Project:** genaiguruyoutube

## Migration Stats
| Item | Count |
|------|-------|
| Flows | 15 |
| Sub Agents | 14 |
| Intents | 31 |
| Entity Types | 5 |
| Webhooks | 2 |
| Tools | 2 |
| Test Cases | 1 |
| Golden Evals | 29 |
| Warnings | 0 |

## Sub-Agents Created
### `service_cost_calculator`
- **CX Flow:** `6e03100f-ab43-482e-a1ce-d76b3cc5fb6d`
- **Description:** Handles: Service cost calculator
- **Pages migrated:** 2
- **Tools used:** none

### `any_think_else`
- **CX Flow:** `81e77d67-3429-4588-a4c7-431bb04a20f3`
- **Description:** Handles: Any Think Else
- **Pages migrated:** 1
- **Tools used:** none

### `care`
- **CX Flow:** `81f9488f-33ce-421e-9dd7-a5807805a11a`
- **Description:** Handles: care
- **Pages migrated:** 1
- **Tools used:** none

### `warrenty`
- **CX Flow:** `859bbc3a-bc99-4f57-8a0d-7ac8e5eb7b5f`
- **Description:** Handles: Warrenty
- **Pages migrated:** 0
- **Tools used:** none

### `general_queries`
- **CX Flow:** `9d8f8b2f-0468-4d10-9f0b-9e83122ac3b2`
- **Description:** Handles: General Queries
- **Pages migrated:** 1
- **Tools used:** none

### `request_test_drive`
- **CX Flow:** `a27af2f7-e0b1-48a2-8443-e1923391e65a`
- **Description:** Handles: Request Test Drive
- **Pages migrated:** 3
- **Tools used:** ['car_connect']

### `complaint_and_feedback`
- **CX Flow:** `ade5c958-81bc-4f45-9dc3-517b4fbe7387`
- **Description:** Handles: Complaint and Feedback
- **Pages migrated:** 4
- **Tools used:** none

### `shield_of_trust`
- **CX Flow:** `b25d8d0e-84f7-4b2d-9337-f818a294123d`
- **Description:** Handles: Shield of Trust
- **Pages migrated:** 0
- **Tools used:** none

### `my_app`
- **CX Flow:** `b8b235fa-0425-4381-bd60-752c40e2c77c`
- **Description:** Handles: My App
- **Pages migrated:** 1
- **Tools used:** none

### `find_dealer`
- **CX Flow:** `cf3c96bf-9f47-4b61-9093-d007998bb8d0`
- **Description:** Handles: Find Dealer
- **Pages migrated:** 6
- **Tools used:** ['car_connect']

### `buy_now`
- **CX Flow:** `d054f7cd-c36e-406e-ab26-d746cbba838a`
- **Description:** Handles: Buy Now
- **Pages migrated:** 1
- **Tools used:** none

### `play_and_win_car`
- **CX Flow:** `d7b3b32f-6cda-4bb3-9bf9-3ec157bc2dc2`
- **Description:** Handles: Play & Win Car
- **Pages migrated:** 4
- **Tools used:** ['car_connect']

### `explore_car`
- **CX Flow:** `dd2e2c19-23ac-489c-8ebe-ebe5df3098f7`
- **Description:** Handles: Explore car
- **Pages migrated:** 1
- **Tools used:** none

### `explore_car_service`
- **CX Flow:** `f53a185e-4456-4108-b533-3cfce028f054`
- **Description:** Handles: Explore Car Service
- **Pages migrated:** 6
- **Tools used:** ['car_connect']

## Tools (from Webhooks)
- **test**: `https://dentrix-759503671462.us-central1.run.app` (NONE)
- **car_connect**: `https://car-connect-907971469140.us-central1.run.app` (NONE)

## Output Files
| File | Description |
|------|-------------|
| `ces_agent.json` | CES agent definition (importable via REST API or Console) |
| `golden_evals.csv` | Test cases in CES batch evaluation CSV format |
| `entity_types.json` | Entity type definitions for manual re-creation in CES |
| `migration_report.md` | This report |

## Next Steps
1. Review `ces_agent.json` and update tool endpoints in the `tools` section
2. Import agent via CES Console: Console > Import Agent > Upload JSON
3. Upload `golden_evals.csv` via: Evaluate tab > + Add test case > Golden > Upload file
4. Re-create entity types from `entity_types.json` as CES does not have a direct import path
5. Update webhook URLs in each tool definition to point to your live endpoints
6. Run evaluation suite and review pass rates