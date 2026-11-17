# canEYE actions

Pass the action name (left) to `caneye.sh check`. If nothing here fits, use the closest one; an
action canEYE doesn't recognise is answered "ask first".

| Area | Action | What it covers | Example summary |
|---|---|---|---|
| Calendar | `calendar.read` | Read events | "Look at Friday's schedule" |
| | `calendar.add_event` | Add events | "Add dentist Friday 3pm" |
| | `calendar.change_event` | Change events | "Move standup to 10am" |
| | `calendar.cancel_event` | Cancel events | "Cancel Tuesday's 1:1 with Sam" |
| Email | `email.read` | Read email | "Read today's unread email" |
| | `email.draft` | Draft and handle routine email | "Draft a reply to the plumber" |
| | `email.send` | Send email | "Email my landlord that rent is late" |
| | `email.delete` | Delete email | "Delete the newsletters from last week" |
| Shopping | `shopping.research` | Research purchases | "Compare noise-cancelling headphones" |
| | `shopping.reorder` | Reorder routine items | "Reorder dish soap" |
| | `shopping.buy` | Make purchases | "Buy AirPods on Amazon for $249" |
| Travel | `travel.search` | Search travel | "Find flights to Denver in May" |
| | `travel.book` | Book travel | "Book the 8am United flight, $312" |
| Files | `files.search` | Search files | "Find the lease PDF" |
| | `files.read` | Read files | "Read the budget spreadsheet" |
| | `files.create` | Create files | "Create a packing list doc" |
| | `files.edit` | Edit files | "Update the budget totals" |
| | `files.delete` | Delete files | "Delete old drafts folder" |
| | `files.share_internal` | Share files inside the user's organization | "Share the deck with Priya" |
| | `files.share_external` | Share files outside the organization | "Share the contract with the buyer's agent" |
| Chat & messaging | `messaging.read` | Read chat messages | "Read the family group chat" |
| | `messaging.draft` | Draft chat messages | "Draft a Slack reply to Ana" |
| | `messaging.send` | Send chat messages | "Text Mom I'm running late" |
| | `messaging.delete` | Delete chat messages | "Delete my last message" |
| Shared workspaces | `collaboration.read` | Read shared pages | "Read the project wiki" |
| | `collaboration.create` | Create shared pages | "Create a meeting notes page" |
| | `collaboration.edit` | Edit shared pages | "Update the roadmap page" |
| | `collaboration.delete` | Delete shared pages | "Delete the old FAQ page" |
| | `collaboration.publish` | Publish pages | "Publish the launch post" |
| | `collaboration.share` | Share workspaces | "Invite the contractor to the workspace" |
| Customer records | `crm.read` / `crm.create` / `crm.update` / `crm.delete` | Read, create, update, delete customer records | "Update Acme's phone number" |
| Tasks & tickets | `tasks.read` / `tasks.create` / `tasks.update` / `tasks.delete` | Read, create, update, delete tasks | "Close ticket #482" |
| Bills & subscriptions | `bills.pay` | Pay bills (needs amount and payee) | "Pay City Power $84.20" |
| | `bills.subscribe` | Start subscriptions | "Start a Netflix subscription" |
| Access and other AIs | `access.credentials` | Use saved passwords and keys | "Log in to the bank with saved password" |
| | `access.connect_tool` | Connect a new app or tool | "Connect Zapier to Gmail" |
| | `access.handoff` | Hand tasks to another AI | "Ask another agent to book the hotel" |
| Always needs okay | `documents.sign` | Sign agreements | "Sign the lease renewal" |
| | `money.transfer` | Move money (needs amount and recipient) | "Send $200 to Alex on Venmo" |

`documents.sign` and `money.transfer` are never automatic, whatever the rules say.
