## Description: <br>
Build and debug ARKit features for visionOS, including ARKitSession setup, authorization, data providers (world tracking, plane detection, scene reconstruction, hand tracking), anchor processing, and RealityKit integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomkrikorian](https://clawhub.ai/user/tomkrikorian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement and debug ARKitSession-based visionOS features, choose appropriate ARKit data providers, handle authorization, process anchors, and bridge ARKit data into RealityKit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated app guidance may involve camera, hand-tracking, world-sensing, room, scene reconstruction, or shared spatial permissions. <br>
Mitigation: Review requested permissions before shipping, provide clear user-facing permission text, and handle denied authorization cleanly. <br>
Risk: Sensor data from ARKit providers can expose sensitive information if retained or transmitted unnecessarily. <br>
Mitigation: Avoid retaining or transmitting sensor data unless it is necessary for the feature. <br>


## Reference(s): <br>
- [ARKit visionOS Code Patterns](references/REFERENCE.md) <br>
- [WorldTrackingProvider](references/world-tracking-provider.md) <br>
- [HandTrackingProvider](references/hand-tracking-provider.md) <br>
- [PlaneDetectionProvider](references/plane-detection-provider.md) <br>
- [SceneReconstructionProvider](references/scene-reconstruction-provider.md) <br>
- [ImageTrackingProvider](references/image-tracking-provider.md) <br>
- [ObjectTrackingProvider](references/object-tracking-provider.md) <br>
- [RoomTrackingProvider](references/room-tracking-provider.md) <br>
- [AccessoryTrackingProvider](references/accessory-tracking-provider.md) <br>
- [BarcodeDetectionProvider](references/barcode-detection-provider.md) <br>
- [CameraFrameProvider](references/camera-frame-provider.md) <br>
- [CameraRegionProvider](references/camera-region-provider.md) <br>
- [EnvironmentLightEstimationProvider](references/environment-light-estimation-provider.md) <br>
- [SharedCoordinateSpaceProvider](references/shared-coordinate-space-provider.md) <br>
- [StereoPropertiesProvider](references/stereo-properties-provider.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Swift code examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
