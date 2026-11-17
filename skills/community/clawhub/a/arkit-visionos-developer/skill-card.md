## Description:

Build and debug ARKit features for visionOS, including ARKitSession setup, authorization, data providers, anchor processing, and RealityKit integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomkrikorian](https://clawhub.ai/user/tomkrikorian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement or troubleshoot ARKit workflows on visionOS, including session setup, provider authorization, anchor updates, and RealityKit integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated app code may access camera, hand, room, or spatial environment data in a visionOS app.

Mitigation: Review generated code, Info.plist usage descriptions, authorization handling, and user-facing permission prompts before deployment.

Risk: Some ARKit providers require device support, specific presentation modes, entitlements, or enterprise licensing.

Mitigation: Check provider support and required authorizations at runtime, and confirm entitlements or licensing before enabling provider-specific features.

## Reference(s):

- [ARKit visionOS Code Patterns](references/REFERENCE.md)
- [WorldTrackingProvider](references/world-tracking-provider.md)
- [HandTrackingProvider](references/hand-tracking-provider.md)
- [PlaneDetectionProvider](references/plane-detection-provider.md)
- [SceneReconstructionProvider](references/scene-reconstruction-provider.md)
- [ImageTrackingProvider](references/image-tracking-provider.md)
- [ObjectTrackingProvider](references/object-tracking-provider.md)
- [RoomTrackingProvider](references/room-tracking-provider.md)
- [AccessoryTrackingProvider](references/accessory-tracking-provider.md)
- [BarcodeDetectionProvider](references/barcode-detection-provider.md)
- [CameraFrameProvider](references/camera-frame-provider.md)
- [CameraRegionProvider](references/camera-region-provider.md)
- [EnvironmentLightEstimationProvider](references/environment-light-estimation-provider.md)
- [SharedCoordinateSpaceProvider](references/shared-coordinate-space-provider.md)
- [StereoPropertiesProvider](references/stereo-properties-provider.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown responses with Swift code snippets and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated app code may involve camera, hand, room, and spatial environment permissions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
