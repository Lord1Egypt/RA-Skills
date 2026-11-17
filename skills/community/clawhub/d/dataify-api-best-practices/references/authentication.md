# Authentication

Read `DATAIFY_API_TOKEN` from the process environment and send `Authorization: Bearer <value>`. Never accept it through a public CLI flag, write it to logs, include it in generated examples, or ask a user to paste it into chat. Treat 401/403 as invalid credentials and 402 as insufficient balance; only a missing credential should show the registration offer.
