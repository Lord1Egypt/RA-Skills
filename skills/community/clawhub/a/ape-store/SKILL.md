\---

name: apestore-token-creator

description: Deploys a real token on Ape.Store on the BASE blockchain. Use when user wants to create or deploy a token on ape.store.

\---



\# Ape.Store Token Creator



When the user asks to create a token on Ape.Store, use the bash tool to run this exact command:



bash command:"node \\"C:\\Users\\ben\\.openclaw\\workspace\\skills\\ape-store\\index.js\\" create a token on ape.store with the name NAME and the symbol SYMBOL and the description DESCRIPTION"



Replace NAME, SYMBOL, DESCRIPTION with the user's actual inputs. If an image path is provided append: and image IMAGE\_PATH



\## RULES

\- ALWAYS run the bash command above using the bash tool

\- NEVER mock, simulate or generate fake output

\- NEVER create metadata.json or copy image files yourself

\- Wait for real output containing TX Hash and Block number

\- Report the TX Hash and Block number back to the user as confirmation

