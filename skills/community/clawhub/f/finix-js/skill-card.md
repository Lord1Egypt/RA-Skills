## Description: <br>
Finix.js integration for accepting card and ACH bank payments on the web, including hosted payment form embedding, browser tokenization, and server-side token exchange for Buyer Identities, Payment Instruments, Transfers, and Authorizations via the Finix Payments API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jbryant](https://clawhub.ai/user/jbryant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Finix checkout flows to websites, including hosted card or ACH collection, payment tokenization, fraud session forwarding, and backend charge or authorization handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated payment-flow guidance or code could create real charges or transfers when paired with live Finix credentials. <br>
Mitigation: Start in sandbox, review charge and transfer logic before production use, and restrict or rotate payment credentials as live payment API secrets. <br>
Risk: FINIX_USERNAME and FINIX_PASSWORD are sensitive credentials. <br>
Mitigation: Keep API credentials strictly server-side, store them in protected environment variables or a secrets manager, and never include them in browser-delivered code. <br>
Risk: Incorrect handling of card or bank data can increase payment-compliance exposure. <br>
Mitigation: Use Finix.js hosted tokenization so raw card and bank data does not touch merchant servers, serve production pages over HTTPS, and verify the final integration against Finix documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jbryant/finix-js) <br>
- [Finix homepage](https://finix.com) <br>
- [Finix.js tokenization guide](https://docs.finix.com/guides/online-payments/payment-tokenization/tokenization-forms) <br>
- [Create an Identity](https://docs.finix.com/api/identities/createidentity) <br>
- [Create a Payment Instrument](https://docs.finix.com/api/payment-instruments/createpaymentinstrument) <br>
- [Create a Transfer](https://docs.finix.com/api/transfers/createtransfer) <br>
- [Create an Authorization](https://docs.finix.com/api/authorizations/createauthorization) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript, HTML, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Finix sandbox and production configuration guidance plus environment-variable names for server-side credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
