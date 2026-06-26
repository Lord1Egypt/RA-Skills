## Description: <br>
Generate React components that render FOSMVVM ViewModels. Scaffolds ViewModelView pattern with hooks, loading states, and TypeScript types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foscomputerservices](https://clawhub.ai/user/foscomputerservices) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to scaffold React views and matching Jest/React Testing Library tests for FOSMVVM ViewModels. It is intended for new FOSMVVM UI components, Leaf-to-React migrations, forms, lists, and other views whose ViewModel and ServerRequest details are already understood from project context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated form submissions or viewModel.operations calls may wire the wrong action if the conversation or specification context is incomplete. <br>
Mitigation: Review generated diffs against the intended ViewModel and ServerRequest behavior before committing or running the new code. <br>
Risk: Generated component and test files may not match the local project conventions or runtime expectations. <br>
Mitigation: Run the generated tests and inspect the component wrapper, .bind() calls, error ViewModel handling, and navigation intents before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/foscomputerservices/fosmvvm-react-view-generator) <br>
- [FOSUtilities homepage](https://github.com/foscomputerservices/FOSUtilities) <br>
- [reference.md](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Guidance] <br>
**Output Format:** [React JSX and Jest test source files with brief verification guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a component test file before the React implementation and expects ViewModel and ServerRequest details to be available from conversation or specification context.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
