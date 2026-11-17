# VFAT/Sickle execution checks

Apply the normal exact-authorization and receipt gates to a user-selected VFAT route. These checks do not add financial authority. Reviewed 2026-09-05.

Before requesting a signature, bind the complete unsigned plan to the current Sickle owner, operator approval, registry, strategy, connector, pool/gauge, token approvals, fee configuration, recipients and automation state. Read deployed code and current state; an upstream audit or interface label is insufficient.

Decode the whole batched route. Separate account creation, permission changes, swaps, LP/NFT transfers, staking, reward fees and residue transfers. Simulate from the actual sender with exact calldata and native value. Stop if the interface or connected tool hides these terms, changes the approved route, or substitutes a wrapper/reward router that the user did not choose.

Enabling an approved operator, per-position automation, NFT operator approval or a fee-bearing ownership wrapper must be included in the reviewed effects. A deposit request is not general permission to enable every available automation feature. Do not treat a documented rebalance stop-loss as an exit instruction.

Submit only the confirmed step once. After a mined receipt, reconcile account ownership, LP/NFT identity, staking state, net rewards, paid fees, residual balances and actual automation settings. Rebuild dependent steps from that state. A reminted NFT may inherit automation; reread it rather than assuming permissions reset.

For exit or recovery, verify the selected withdrawal/sweep path and output recipient before submission. Principal and rewards can follow different paths in wrapper-based integrations. A failure to find a position on the website is not evidence it was withdrawn. Never retry an unknown submission or report completion from a success banner alone.

Sources: [Sickle architecture](https://docs.vfat.io/sickle/), [fee model](https://docs.vfat.io/fees/), [automation](https://docs.vfat.io/automation/), and [official wrapper source](https://github.com/vfat-io/sickle-wrapper).
